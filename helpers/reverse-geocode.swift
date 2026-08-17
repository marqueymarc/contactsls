import CoreLocation
import Foundation

for line in String(data: FileHandle.standardInput.readDataToEndOfFile(), encoding: .utf8)!.split(separator: "\n") {
    let values = line.split(separator: ",")
    guard values.count == 2, let latitude = Double(values[0]), let longitude = Double(values[1]) else { continue }
    let semaphore = DispatchSemaphore(value: 0)
    var label = ""
    CLGeocoder().reverseGeocodeLocation(CLLocation(latitude: latitude, longitude: longitude)) { placemarks, _ in
        if let placemark = placemarks?.first {
            label = [placemark.name, placemark.locality, placemark.administrativeArea]
                .compactMap { $0 }.reduce(into: []) { if !$0.contains($1) { $0.append($1) } }.joined(separator: ", ")
        }
        semaphore.signal()
    }
    while semaphore.wait(timeout: .now()) != .success {
        RunLoop.current.run(until: Date(timeIntervalSinceNow: 0.1))
    }
    print("\(latitude),\(longitude)\t\(label)")
}
