const express = require("express")
const fs = require("fs")
const { exec } = require("child_process")
const path = require("path")
const os = require("os")
const axios = require("axios")
const { createObjectCsvWriter } = require("csv-writer")

const app = express()

app.use(express.json())
app.use(express.static("public"))

const TEMP_DIR = "./runner/temp"

const hardware = require("./data/hardwarePower.json")
const carbonData = require("./data/carbonIntensity.json")

let selectedCountry = "India"

const csvWriter = createObjectCsvWriter({
    path: "./data/executionDataset.csv",
    header: [
        { id: "timestamp", title: "timestamp" },
        { id: "activity", title: "activity" },
        { id: "language", title: "language" },
        { id: "executionTime", title: "executionTime" },
        { id: "cpuUsage", title: "cpuUsage" },
        { id: "energy", title: "energy" },
        { id: "co2", title: "co2" },
        { id: "carbonIntensity", title: "carbonIntensity" }
    ],
    append: true
})


function getCPUUsage() {

    const cpus = os.cpus()

    let idle = 0
    let total = 0

    cpus.forEach(core => {

        for (let type in core.times) {
            total += core.times[type]
        }

        idle += core.times.idle

    })

    return { idle, total }

}


async function getRealtimeCarbonIntensity() {

    try {

        const response = await axios.get(
            "https://api.carbonintensity.org.uk/intensity"
        )

        const realtime = response.data.data[0].intensity.actual

        return realtime

    } catch (error) {
        return carbonData[selectedCountry]

    }

}


function estimateEnergy(execTime, cpuUsage, carbonIntensity){

const P_idle = hardware.cpu_idle
const P_max = hardware.cpu_max

const cpuPower = P_idle + (P_max - P_idle) * (cpuUsage/100)

const ramPower = hardware.ram
const diskPower = hardware.disk

const totalPower = cpuPower + ramPower + diskPower

const energyWh = totalPower * (execTime/3600)

const energyKwh = energyWh / 1000

const co2 = energyKwh * carbonIntensity

return {energyKwh, co2, totalPower}

}



app.post("/run", async (req, res) => {

const { code, lang, activity = "coding" } = req.body

let filePath
let command

if (lang === "python") {

const id = Date.now()
filePath = path.join(TEMP_DIR, `temp_${id}.py`)

fs.writeFileSync(filePath, code)

command = `python ${filePath}`

}

else if (lang === "cpp") {

const id = Date.now()
filePath = path.join(TEMP_DIR, `temp_${id}.cpp`)

const exePath = path.join(TEMP_DIR, `temp_${id}.exe`)

fs.writeFileSync(filePath, code)

command = `g++ "${filePath}" -o "${exePath}" && "${exePath}"`

}


const startCPU = getCPUUsage()
const startTime = process.hrtime()


exec(command, async (err, stdout, stderr) => {

    const diff = process.hrtime(startTime)
    const execTime = diff[0] + diff[1] / 1e9

    const endCPU = getCPUUsage()

    const idleDiff = endCPU.idle - startCPU.idle
    const totalDiff = endCPU.total - startCPU.total

    const cpuUsage = 100 - Math.floor(100 * idleDiff / totalDiff)

    const carbonIntensity = await getRealtimeCarbonIntensity()

    const result = estimateEnergy(execTime, cpuUsage, carbonIntensity)

    await csvWriter.writeRecords([
    {
        timestamp: new Date().toISOString(),
        activity: activity,
        language: lang,
        executionTime: execTime,
        cpuUsage: cpuUsage,
        energy: result.energyKwh,
        co2: result.co2,
        carbonIntensity: carbonIntensity
    }
    ])

    res.json({
        output: stdout || stderr,
        executionTime: execTime,
        cpuUsage: cpuUsage,
        energy: result.energyKwh,
        co2: result.co2,
        carbonIntensity: carbonIntensity
    })

})

})



app.listen(3000,()=>{

console.log("Server running at http://localhost:3000")

})