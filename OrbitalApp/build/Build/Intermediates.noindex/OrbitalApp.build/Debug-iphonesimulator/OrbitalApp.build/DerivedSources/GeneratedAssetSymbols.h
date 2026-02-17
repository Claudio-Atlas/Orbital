#import <Foundation/Foundation.h>

#if __has_attribute(swift_private)
#define AC_SWIFT_PRIVATE __attribute__((swift_private))
#else
#define AC_SWIFT_PRIVATE
#endif

/// The "GoogleLogo" asset catalog image resource.
static NSString * const ACImageNameGoogleLogo AC_SWIFT_PRIVATE = @"GoogleLogo";

/// The "OrbitalLogo" asset catalog image resource.
static NSString * const ACImageNameOrbitalLogo AC_SWIFT_PRIVATE = @"OrbitalLogo";

/// The "OrbitalLogoDark" asset catalog image resource.
static NSString * const ACImageNameOrbitalLogoDark AC_SWIFT_PRIVATE = @"OrbitalLogoDark";

#undef AC_SWIFT_PRIVATE
