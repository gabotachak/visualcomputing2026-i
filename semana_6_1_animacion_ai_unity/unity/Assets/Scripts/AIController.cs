using UnityEngine;
using UnityEngine.AI;

namespace AI
{
    public enum AIState
    {
        Idle,
        Patrol,
        Chase
    }

    [RequireComponent(typeof(NavMeshAgent))]
    [RequireComponent(typeof(Animator))]
    public class AIController : MonoBehaviour
    {
        [Header("Patrol Settings")]
        [Tooltip("Points the agent will patrol between.")]
        public Transform[] waypoints;
        public float waypointTolerance = 0.5f;
        public float idleDuration = 2f;

        [Header("Detection Settings")]
        public Transform player;
        public float detectionRadius = 10f;
        public float loseRadius = 15f;
        
        [Header("Debug")]
        public bool showGizmos = true;

        private NavMeshAgent agent;
        private Animator animator;
        private AIState currentState = AIState.Idle;
        private int currentWaypointIndex = 0;
        private float idleTimer = 0f;

        private void Start()
        {
            agent = GetComponent<NavMeshAgent>();
            animator = GetComponent<Animator>();

            if (player == null)
            {
                // Try to find the player by tag
                GameObject playerObj = GameObject.FindWithTag("Player");
                if (playerObj != null)
                {
                    player = playerObj.transform;
                }
            }

            // Set initial state
            currentState = AIState.Idle;
            SetNextWaypointDestination();
        }

        private void Update()
        {
            if (player == null) return;

            // Sincronizar la velocidad del agente con el parámetro "Speed" del Animator
            float speed = agent.velocity.magnitude;
            animator.SetFloat("Speed", speed);

            // Control de transiciones de estados
            switch (currentState)
            {
                case AIState.Idle:
                    HandleIdleState();
                    break;
                case AIState.Patrol:
                    HandlePatrolState();
                    break;
                case AIState.Chase:
                    HandleChaseState();
                    break;
            }
        }

        private void HandleIdleState()
        {
            agent.isStopped = true;
            idleTimer += Time.deltaTime;

            // Detección de jugador durante Idle
            if (IsPlayerInRadius(detectionRadius))
            {
                TransitionToState(AIState.Chase);
                return;
            }

            if (idleTimer >= idleDuration)
            {
                TransitionToState(AIState.Patrol);
            }
        }

        private void HandlePatrolState()
        {
            agent.isStopped = false;

            // Comprobar detección de jugador
            if (IsPlayerInRadius(detectionRadius))
            {
                TransitionToState(AIState.Chase);
                return;
            }

            // Si llegamos al destino actual
            if (!agent.pathPending && agent.remainingDistance <= waypointTolerance)
            {
                TransitionToState(AIState.Idle);
            }
        }

        private void HandleChaseState()
        {
            agent.isStopped = false;
            
            // Perseguir al jugador constantemente
            agent.SetDestination(player.position);

            // Comprobar si se perdió al jugador (sale del radio de pérdida)
            if (!IsPlayerInRadius(loseRadius))
            {
                TransitionToState(AIState.Patrol);
            }
        }

        private void TransitionToState(AIState newState)
        {
            currentState = newState;
            idleTimer = 0f;

            if (newState == AIState.Patrol)
            {
                SetNextWaypointDestination();
            }
            else if (newState == AIState.Idle)
            {
                // Avanzar al siguiente punto para el próximo patrullaje
                if (waypoints.Length > 0)
                {
                    currentWaypointIndex = (currentWaypointIndex + 1) % waypoints.Length;
                }
            }
        }

        private void SetNextWaypointDestination()
        {
            if (waypoints.Length > 0 && waypoints[currentWaypointIndex] != null)
            {
                agent.SetDestination(waypoints[currentWaypointIndex].position);
            }
        }

        private bool IsPlayerInRadius(float radius)
        {
            if (player == null) return false;
            return Vector3.Distance(transform.position, player.position) <= radius;
        }

        private void OnDrawGizmos()
        {
            if (!showGizmos) return;

            // Dibujar radio de detección en amarillo
            Gizmos.color = Color.yellow;
            Gizmos.DrawWireSphere(transform.position, detectionRadius);

            // Dibujar radio de pérdida en rojo
            Gizmos.color = Color.red;
            Gizmos.DrawWireSphere(transform.position, loseRadius);

            // Dibujar líneas a los waypoints en azul
            if (waypoints != null)
            {
                Gizmos.color = Color.blue;
                foreach (var wp in waypoints)
                {
                    if (wp != null)
                    {
                        Gizmos.DrawLine(transform.position, wp.position);
                    }
                }
            }
        }
    }
}
