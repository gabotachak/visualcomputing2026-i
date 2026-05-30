using UnityEngine;
using UnityEngine.UI;

namespace MR
{
    public class WebCamBackground : MonoBehaviour
    {
        [Header("UI Render Target (Optional)")]
        [Tooltip("RawImage in UI Canvas to project the webcam texture.")]
        public RawImage backgroundUI;

        [Header("Mesh Render Target (Optional)")]
        [Tooltip("Renderer of a background plane/quad in the 3D scene.")]
        public Renderer backgroundRenderer;

        [Header("WebCam Settings")]
        public int requestedWidth = 1280;
        public int requestedHeight = 720;
        public int requestedFPS = 30;

        private WebCamTexture webcamTexture;
        private AspectRatioFitter aspectFitter;

        private void Start()
        {
            // Get available camera devices
            WebCamDevice[] devices = WebCamTexture.devices;
            if (devices.length == 0)
            {
                Debug.LogError("No webcam devices detected!");
                return;
            }

            // Print detected devices for debugging
            for (int i = 0; i < devices.Length; i++)
            {
                Debug.Log($"Webcam device [{i}]: {devices[i].name} (FrontFacing: {devices[i].isFrontFacing})");
            }

            // Create WebCamTexture with default/first device
            webcamTexture = new WebCamTexture(devices[0].name, requestedWidth, requestedHeight, requestedFPS);

            // Assign texture to UI RawImage if set
            if (backgroundUI != null)
            {
                backgroundUI.texture = webcamTexture;
                
                // Get or add AspectRatioFitter to prevent stretching
                aspectFitter = backgroundUI.GetComponent<AspectRatioFitter>();
                if (aspectFitter == null)
                {
                    aspectFitter = backgroundUI.gameObject.AddComponent<AspectRatioFitter>();
                }
                aspectFitter.aspectMode = AspectRatioFitter.AspectMode.EnvelopeParent;
            }

            // Assign texture to Mesh Renderer if set
            if (backgroundRenderer != null)
            {
                backgroundRenderer.material.mainTexture = webcamTexture;
            }

            // Start playing webcam video stream
            webcamTexture.Play();
        }

        private void Update()
        {
            if (webcamTexture == null || !webcamTexture.isPlaying) return;

            // Handle aspect ratio dynamic updates and rotation correction (especially on mobile/tablets)
            if (backgroundUI != null && webcamTexture.width > 100)
            {
                // Set correct aspect ratio
                float aspect = (float)webcamTexture.width / (float)webcamTexture.height;
                aspectFitter.aspectRatio = aspect;

                // Adjust UI rotation if camera orientation is offset
                float rotationAngle = -webcamTexture.videoRotationAngle;
                backgroundUI.rectTransform.localEulerAngles = new Vector3(0, 0, rotationAngle);

                // Correct mirror effect for front-facing cameras
                float scaleY = webcamTexture.videoVerticallyMirrored ? -1.0f : 1.0f;
                backgroundUI.rectTransform.localScale = new Vector3(1.0f, scaleY, 1.0f);
            }
        }

        private void OnDestroy()
        {
            if (webcamTexture != null)
            {
                webcamTexture.Stop();
            }
        }
    }
}
