import Contacts
import Foundation

let store = CNContactStore()
let status = CNContactStore.authorizationStatus(for: .contacts)
if status == .notDetermined {
    let semaphore = DispatchSemaphore(value: 0)
    store.requestAccess(for: .contacts) { _, _ in semaphore.signal() }
    semaphore.wait()
}
do {
    for container in try store.containers(matching: nil) {
        print(container.identifier)
    }
} catch {
    fputs("Contacts access failed: \(error)\n", stderr)
    exit(1)
}
