using System.Collections;
using UnityEngine;

namespace UPMPackageDemo
{
    public class Greeter : MonoBehaviour
    {
        private IEnumerator Start()
        {
            const int NO_OF_GREETINGS = 10;
            const float DELAY_PER_GREETING = 0.1f;

            var waitForSeconds = new WaitForSeconds(DELAY_PER_GREETING);

            for (var i = 0; i < NO_OF_GREETINGS; ++i)
            {
                yield return waitForSeconds;
                Greet();
            }
        }

        private void Greet()
        {
            Debug.Log($"Hello! It has been {Time.realtimeSinceStartup:F2} seconds since start up.");
        }
    }
}
