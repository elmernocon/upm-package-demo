using UnityEngine;

namespace UPMPackageDemo
{
    public class Greeter : MonoBehaviour
    {
        private void Start()
        {
            Greet();
        }

        private void Greet()
        {
            Debug.Log($"Hello! It has been {Time.realtimeSinceStartup:F2} seconds since start up.");
        }
    }
}
