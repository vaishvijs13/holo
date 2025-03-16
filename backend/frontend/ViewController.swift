import UIKit
import ARKit

class ViewController: UIViewController, ARSCNViewDelegate {
    @IBOutlet var sceneView: ARSCNView!
    
    override func viewD() {
        super.viewD()
        sceneView.delegate = self
        sceneView.session.run(ARWorldTrackingConfiguration())
        fetchData()
    }

    func fetchData() {
        let url = URL(string: "http://192.168.1.87:5002/track")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        // get the AR frame, then convert to base64 as reqd in server.py
        let image = sceneView.snapshot()
        guard let imageData = image.jpegData(compressionQuality: 0.8)?.base64EncodedString() else { return }

        let jsonBody: [String: Any] = ["image": imageData]
        let jsonData = try? JSONSerialization.data(withJSONObject: jsonBody)

        let task = URLSession.shared.uploadTask(with: request, from: jsonData) { data, response, error in
            guard let data = data, error == nil else { return }
            DispatchQueue.main.async {
                self.processData(data)
            }
        }
        task.resume()
    }

    func processData(_ data: Data) {
        guard let json = try? JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
              let tracked = json["tracked_objects"] as? [String: Any] else { return }
        
        for (_, obj) in tracked {
            guard let objDict = obj as? [String: Any],
                  let label = objDict["label"] as? String,
                  let position = objDict["position"] as? [String: Float] else { continue }
            
            let textNode = SCNText(string: label, extrusionDepth: 1.0)
            let node = SCNNode(geometry: textNode)
            node.position = SCNVector3(x: position["x"] ?? 0.0, 
                                       y: position["y"] ?? 0.0, 
                                       z: -1.0)
            sceneView.scene.rootNode.addChildNode(node)
        }
    }
}