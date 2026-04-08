#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;
using System.IO;

public class DemoCapture : EditorWindow
{
    public static void CaptureGif()
    {
        // 1. Invocar inicialización previa
        ShaderDemoSetup.GenerateDemo();

        // 2. Localizar directorio y configurar cámara y luz
        string outputDir = "/Users/gabotachak/github.com/gabotachak/visualcomputing2026-i/semana_3_4_etapas_pipeline_programable/media/frames";
        if (!Directory.Exists(outputDir)) Directory.CreateDirectory(outputDir);

        GameObject camObj = new GameObject("CaptureCamera");
        camObj.transform.position = new Vector3(0, 1.5f, -4f);
        camObj.transform.LookAt(Vector3.zero);
        Camera cam = camObj.AddComponent<Camera>();
        cam.clearFlags = CameraClearFlags.SolidColor;
        cam.backgroundColor = new Color(0.2f, 0.2f, 0.2f); // Gris oscuro

        GameObject lightObj = new GameObject("DirLight");
        Light light = lightObj.AddComponent<Light>();
        light.type = LightType.Directional;
        lightObj.transform.rotation = Quaternion.Euler(50, -30, 0);

        // 3. RenderTexture para Off-Screen rendering
        RenderTexture rt = new RenderTexture(640, 640, 24);
        cam.targetTexture = rt;
        Texture2D tex = new Texture2D(640, 640, TextureFormat.RGB24, false);

        int frames = 30;
        float timeStep = 0.1f;

        for (int i = 0; i < frames; i++)
        {
            float currentTime = i * timeStep;
            
            // Simular el avance del tiempo inyectando global values
            Material mat = GameObject.Find("EsferaProgramable").GetComponent<Renderer>().sharedMaterial;
            mat.SetFloat("_CustomTime", currentTime);

            cam.Render();

            RenderTexture.active = rt;
            tex.ReadPixels(new Rect(0, 0, 640, 640), 0, 0);
            tex.Apply();
            RenderTexture.active = null;

            byte[] bytes = tex.EncodeToPNG();
            File.WriteAllBytes(Path.Combine(outputDir, $"frame_{i:D3}.png"), bytes);
            Debug.Log($"Guardado Frame {i}");
        }

        Debug.Log("Captura completada. Saliendo desde editor batchmode...");
        EditorApplication.Exit(0);
    }
}
#endif
