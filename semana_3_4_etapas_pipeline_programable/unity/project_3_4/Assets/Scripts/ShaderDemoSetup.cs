#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

public class ShaderDemoSetup : EditorWindow
{
    [MenuItem("VisualComputing/Generar Demo Pipeline Programable (Semana 3-4)")]
    public static void GenerateDemo()
    {
        // Limpiamos los objetos previos con este script si existieran para recrearlos
        GameObject objPrev = GameObject.Find("EsferaProgramable");
        if(objPrev != null) DestroyImmediate(objPrev);
        objPrev = GameObject.Find("EsferaFija");
        if(objPrev != null) DestroyImmediate(objPrev);

        // 1. Esferas
        GameObject sphere = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        sphere.name = "EsferaProgramable";
        sphere.transform.position = new Vector3(-1.5f, 0, 0);
        
        GameObject sphereFija = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        sphereFija.name = "EsferaFija";
        sphereFija.transform.position = new Vector3(1.5f, 0, 0);
        
        // 2. Material del Pipeline Programable
        Shader customShader = Shader.Find("Custom/PipelinePersonalizado");
        if (customShader == null) 
        {
            Debug.LogError("No se encontró el shader 'Custom/PipelinePersonalizado'. Asegúrate de que compliló correctamente.");
            return;
        }

        Material pipelineMat = new Material(customShader);
        pipelineMat.SetColor("_Color", new Color(0.1f, 0.5f, 0.9f));
        pipelineMat.SetFloat("_FresnelPower", 4.0f);
        
        if (!AssetDatabase.IsValidFolder("Assets/Materials"))
            AssetDatabase.CreateFolder("Assets", "Materials");
            
        AssetDatabase.CreateAsset(pipelineMat, "Assets/Materials/PipelineShaderMaterial.mat");
        sphere.GetComponent<Renderer>().sharedMaterial = pipelineMat;
        
        // 3. Material del Pipeline Fijo (Standard Shader nativo)
        Material matFijo = new Material(Shader.Find("Standard"));
        matFijo.color = new Color(0.1f, 0.5f, 0.9f);
        AssetDatabase.CreateAsset(matFijo, "Assets/Materials/PipelineFijoMaterial.mat");
        sphereFija.GetComponent<Renderer>().sharedMaterial = matFijo;
        
        Debug.Log("Demo generada satisfactoriamente. Visualice la 'EsferaProgramable' distorsionada y con Fresnel frente a la 'EsferaFija' estándar.");
    }
}
#endif
