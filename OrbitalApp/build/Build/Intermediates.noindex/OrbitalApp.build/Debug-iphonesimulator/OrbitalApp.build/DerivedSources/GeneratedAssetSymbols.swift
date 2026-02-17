import Foundation
#if canImport(DeveloperToolsSupport)
import DeveloperToolsSupport
#endif

#if SWIFT_PACKAGE
private let resourceBundle = Foundation.Bundle.module
#else
private class ResourceBundleClass {}
private let resourceBundle = Foundation.Bundle(for: ResourceBundleClass.self)
#endif

// MARK: - Color Symbols -

@available(iOS 17.0, macOS 14.0, tvOS 17.0, watchOS 10.0, *)
extension DeveloperToolsSupport.ColorResource {

}

// MARK: - Image Symbols -

@available(iOS 17.0, macOS 14.0, tvOS 17.0, watchOS 10.0, *)
extension DeveloperToolsSupport.ImageResource {

    /// The "GoogleLogo" asset catalog image resource.
    static let googleLogo = DeveloperToolsSupport.ImageResource(name: "GoogleLogo", bundle: resourceBundle)

    /// The "OrbitalLogo" asset catalog image resource.
    static let orbitalLogo = DeveloperToolsSupport.ImageResource(name: "OrbitalLogo", bundle: resourceBundle)

    /// The "OrbitalLogoDark" asset catalog image resource.
    static let orbitalLogoDark = DeveloperToolsSupport.ImageResource(name: "OrbitalLogoDark", bundle: resourceBundle)

}

