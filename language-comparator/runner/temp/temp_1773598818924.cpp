#include <stdio.h>

#define MAX_NODES 100

int adjMatrix[MAX_NODES][MAX_NODES]; 
int visited[MAX_NODES];              
int queue[MAX_NODES];                

void addEdge(int start, int end)
{
    adjMatrix[start][end] = 1;
    adjMatrix[end][start] = 1; 
}

void bfs(int start, int num_nodes)
{
    int front = 0, rear = 0;
    queue[rear++] = start;
    visited[start] = 1;

    printf("BFS Traversal: ");

    while (front < rear)
    {
        int current = queue[front++];
        printf("%d ", current);
        for (int i = 0; i < num_nodes; i++)
        {
            if (adjMatrix[current][i] == 1 && !visited[i])
            {
                queue[rear++] = i;
                visited[i] = 1;
            }
        }
    }
    printf("\n");
}

int main()
{
    int num_nodes, num_edges;

    printf("Enter the number of nodes: ");
    scanf("%d", &num_nodes);
    printf("Enter the number of edges: ");
    scanf("%d", &num_edges);
    for (int i = 0; i < num_nodes; i++)
    {
        for (int j = 0; j < num_nodes; j++)
        {
            adjMatrix[i][j] = 0;
        }
        visited[i] = 0;
    }
    printf("Enter edges in format (start end):\n");
    for (int i = 0; i < num_edges; i++)
    {
        int start, end;
        scanf("%d %d", &start, &end);
        addEdge(start, end);
    }

    int start_node;
    printf("Enter the starting node for BFS: ");
    scanf("%d", &start_node);

    bfs(start_node, num_nodes);

    return 0;
}
