public class Graph
{
    private int vertices;
    private List<Edge>[] adjacencyList;

    public Graph(int vertices)
    {
        this.vertices = vertices;
        adjacencyList = new List<Edge>[vertices];

        for (int i = 0; i < vertices; i++)
            adjacencyList[i] = new List<Edge>();
    }

    public void AddEdge(int source, int destination, double probability)
    {
        adjacencyList[source].Add(new Edge(destination, probability));
        adjacencyList[destination].Add(new Edge(source, probability)); // If the graph is undirected
    }

    public List<int> FindMostReliablePath(int startVertex, int endVertex)
    {
        double[] probabilities = new double[vertices];
        int[] previous = new int[vertices];
        bool[] visited = new bool[vertices];

        for (int i = 0; i < vertices; i++)
        {
            probabilities[i] = 0;
            previous[i] = -1;
            visited[i] = false;
        }

        probabilities[startVertex] = 1;

        for (int i = 0; i < vertices - 1; i++)
        {
            int currentVertex = GetNextVertexWithMaxProbability(probabilities, visited);
            visited[currentVertex] = true;

            foreach (Edge edge in adjacencyList[currentVertex])
            {
                int neighbor = edge.Destination;
                double edgeProbability = edge.Probability;

                if (!visited[neighbor] && probabilities[currentVertex] * edgeProbability > probabilities[neighbor])
                {
                    probabilities[neighbor] = probabilities[currentVertex] * edgeProbability;
                    previous[neighbor] = currentVertex;
                }
            }
        }

        return BuildPath(previous, startVertex, endVertex);
    }

    private int GetNextVertexWithMaxProbability(double[] probabilities, bool[] visited)
    {
        double maxProbability = 0;
        int maxVertex = -1;

        for (int i = 0; i < vertices; i++)
        {
            if (!visited[i] && probabilities[i] > maxProbability)
            {
                maxProbability = probabilities[i];
                maxVertex = i;
            }
        }

        return maxVertex;
    }

    private List<int> BuildPath(int[] previous, int startVertex, int endVertex)
    {
        List<int> path = new List<int>();
        int currentVertex = endVertex;

        while (currentVertex != -1)
        {
            path.Insert(0, currentVertex);
            currentVertex = previous[currentVertex];
        }

        return path;
    }
}

public class Edge
{
    public int Destination { get; }
    public double Probability { get; }

    public Edge(int destination, double probability)
    {
        Destination = destination;
        Probability = probability;
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        // Read input
        string[] graphData = Console.ReadLine().Split(' ');
        int numVertices = Int32.Parse(graphData[0]);
        int numEdges = Int32.Parse(graphData[1]);

        Graph graph = new Graph(numVertices);

        for (int i = 0; i < numEdges; i++)
        {
            string[] edgeData = Console.ReadLine().Split(' ');
            int source = Int32.Parse(edgeData[0]);
            int destination = Int32.Parse(edgeData[1]);
            double probability = double.Parse(edgeData[2], System.Globalization.CultureInfo.InvariantCulture);

            graph.AddEdge(source, destination, probability);
        }

        int numTests = int.Parse(Console.ReadLine());

        for (int i = 0; i < numTests; i++)
        {
            string[] testData = Console.ReadLine().Split(' ');
            int startVertex = int.Parse(testData[0]);
            int endVertex = int.Parse(testData[1]);

            List<int> path = graph.FindMostReliablePath(startVertex, endVertex);
            Console.WriteLine(string.Join(" ", path));
        }
    }
}