using UnityEngine;

namespace PhysicsEffects
{
    [RequireComponent(typeof(Collider))]
    public class ColisionParticulas : MonoBehaviour
    {
        [Header("Effects Settings")]
        [Tooltip("The particle system to instantiate/play upon collision.")]
        public ParticleSystem collisionParticles;

        [Header("Audio Settings")]
        [Tooltip("Optional audio clip to play on impact.")]
        public AudioClip impactSound;
        private AudioSource audioSource;

        private void Start()
        {
            // Set up audio source if an impact sound is assigned
            if (impactSound != null)
            {
                audioSource = gameObject.AddComponent<AudioSource>();
                audioSource.playOnAwake = false;
                audioSource.spatialBlend = 1.0f; // 3D sound spatialization
            }

            // Ensure the particles don't play on start automatically
            if (collisionParticles != null)
            {
                var main = collisionParticles.main;
                main.playOnAwake = false;
            }
        }

        private void OnCollisionEnter(Collision collision)
        {
            if (collision.contacts.Length > 0)
            {
                ContactPoint contact = collision.contacts[0];
                Vector3 contactPoint = contact.point;
                Vector3 contactNormal = contact.normal;

                // Move particle system to the exact contact point
                if (collisionParticles != null)
                {
                    collisionParticles.transform.position = contactPoint;
                    
                    // Align particles to point away from the surface normal
                    collisionParticles.transform.rotation = Quaternion.LookRotation(contactNormal);
                    
                    // Play the particles
                    collisionParticles.Play();
                }

                // Play sound effect
                if (audioSource != null && impactSound != null)
                {
                    audioSource.PlayOneShot(impactSound);
                }

                Debug.Log($"[Physics Collision] Collided with {collision.gameObject.name} at point {contactPoint}. Particle effect played.");
            }
        }
    }
}
