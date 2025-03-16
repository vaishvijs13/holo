import ARKit

class ARObjectManager {
    static let shared = ARObjectManager()
    
    private init() {}

    func addObject(to sceneView: ARSCNView, with label: String, at position: SCNVector3) {
        let textGeometry = SCNText(string: label, extrusionDepth: 1.0)
        let material = SCNMaterial()
        material.diffuse.contents = UIColor.blue
        textGeometry.materials = [material]

        let textNode = SCNNode(geometry: textGeometry)
        textNode.position = position
        textNode.scale = SCNVector3(0.01, 0.01, 0.01)
        
        sceneView.scene.rootNode.addChildNode(textNode)
    }
}
