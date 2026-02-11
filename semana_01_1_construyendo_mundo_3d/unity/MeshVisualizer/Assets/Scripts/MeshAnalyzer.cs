using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
#endif

[RequireComponent(typeof(MeshFilter))]
public class MeshAnalyzer : MonoBehaviour
{
    [Header("Configuración Visual")]
    [Tooltip("Activa para ver la malla de alambre en la escena (requiere Gizmos activados)")]
    public bool mostrarWireframe = true;
    public Color colorWireframe = Color.cyan;

    private Mesh mesh;

    void Start()
    {
        mesh = GetComponent<MeshFilter>().sharedMesh;

        if (mesh == null)
        {
            Debug.LogError("No se encontró una malla en el MeshFilter.");
            return;
        }

        ImprimirDatosMalla();
    }

    void ImprimirDatosMalla()
    {
        int vertices = mesh.vertexCount;
        int subMallas = mesh.subMeshCount;
        int triangulosTotal = 0;

        // Sumar triángulos de TODOS los sub-meshes
        for (int i = 0; i < subMallas; i++)
        {
            int[] tris = mesh.GetTriangles(i);
            int trisCount = tris.Length / 3;
            triangulosTotal += trisCount;

            // Debug por sub-mesh (opcional, quita si no quieres)
            Debug.Log($"Sub-mesh {i}: {trisCount} triángulos");
        }

        Debug.Log($"--- Análisis del Modelo: {gameObject.name} ({subMallas} sub-meshes) ---");
        Debug.Log($"<color=green>Vértices totales:</color> {vertices} (compartidos)");
        Debug.Log($"<color=yellow>Triángulos totales:</color> {triangulosTotal}");
        Debug.Log($"<color=orange>Sub-mallas:</color> {subMallas}");
        Debug.Log("-------------------------------------------");
    }

    // Visualización mediante Gizmos (YA dibuja TODOS los sub-meshes)
    void OnDrawGizmos()
    {
        if (!mostrarWireframe) return;

        MeshFilter mf = GetComponent<MeshFilter>();
        if (mf == null) return;

        Mesh m = mf.sharedMesh;
        if (m == null) return;

        Gizmos.matrix = transform.localToWorldMatrix;
        Gizmos.color = colorWireframe;

        // Dibuja TODO el mesh con TODOS sus sub-meshes
        Gizmos.DrawWireMesh(m, Vector3.zero, Quaternion.identity, Vector3.one);
    }

    // Método público para el botón de la UI (toggle para TODO el modelo)
    public void AlternarVisualizacion()
    {
        mostrarWireframe = !mostrarWireframe;

#if UNITY_EDITOR
        SceneView.RepaintAll();  // Refresca Scene View
#endif
    }
}
