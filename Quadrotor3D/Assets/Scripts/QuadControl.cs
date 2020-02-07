using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class QuadControl : MonoBehaviour
{
	public Rigidbody rb;

    // Start is called before the first frame update
    void Start()
    {
    	Physics.gravity = new Vector3(0, -9.8f, 0);
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        rb.AddForce(0,9.8f,0, ForceMode.Acceleration);
        
    }
}
