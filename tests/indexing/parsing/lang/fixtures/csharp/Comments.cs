namespace Net;

public class Client
{
    /// <summary>Builds the request path.</summary>
    public string BuildPath(string resource, int id)
    {
        // combine the resource and identifier
        string path = resource + "/" + id;
        /* the default endpoint, not a comment */
        string endpoint = "https://api.example.com // v1";
        return endpoint + "/" + path;
    }
}
