import Foundation

class UnityTo {
    static let shared = UnityTo()
    
    func sendObjectData(objectName: String, position: [Float]) {
        guard let url = URL(string: "http://192.168.1.87:5002/unity-track") else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let jsonBody: [String: Any] = [
            "object_name": objectName,
            "position": ["x": position[0], "y": position[1], "z": position[2]]
        ]
        
        let jsonData = try? JSONSerialization.data(withJSONObject: jsonBody)

        let task = URLSession.shared.uploadTask(with: request, from: jsonData) { data, response, error in
            if let error = error {
                print("Error sending Unity object data: \(error)")
                return
            }
            print("Successfully sent Unity object data to Python server")
        }
        task.resume()
    }
}
