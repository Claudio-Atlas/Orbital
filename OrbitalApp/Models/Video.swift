//
//  Video.swift
//  Orbital - AI Math Video Solver
//
//  Model representing a generated solution video.
//  Videos auto-expire after 48 hours (stored in Cloudflare R2).
//
//  Copyright © 2026 Onyx Enterprises. All rights reserved.
//

import Foundation

/// A generated math solution video with metadata and expiration tracking.
struct Video: Identifiable {
    let id: UUID
    let problem: String
    let category: String
    let subcategory: String
    let durationSeconds: Int
    let stepPreview: [String]
    let result: String?
    let createdAt: Date
    let expiresAt: Date
    let videoURL: URL?
    
    var durationFormatted: String {
        let minutes = durationSeconds / 60
        let seconds = durationSeconds % 60
        return String(format: "%d:%02d", minutes, seconds)
    }
    
    var hoursUntilExpiration: Int {
        let interval = expiresAt.timeIntervalSince(Date())
        return max(0, Int(interval / 3600))
    }
    
    var isExpired: Bool {
        expiresAt < Date()
    }
    
    // Sample data for previews
    static let sampleVideos: [Video] = [
        Video(
            id: UUID(),
            problem: "Find the derivative of x³ + 2x² - 5x + 1",
            category: "Calculus",
            subcategory: "Derivatives",
            durationSeconds: 192,
            stepPreview: ["Differentiate x³, 2x², and -5x", "Apply power rule to each term"],
            result: "3x² + 4x - 5",
            createdAt: Date().addingTimeInterval(-3600),
            expiresAt: Date().addingTimeInterval(72 * 3600), // 3 days
            videoURL: nil
        ),
        Video(
            id: UUID(),
            problem: "Solve for x: 3x - 7 = 14",
            category: "Algebra",
            subcategory: "Linear Equations",
            durationSeconds: 108,
            stepPreview: ["Add 7 to both sides", "Divide both sides by 3"],
            result: "x = 7",
            createdAt: Date().addingTimeInterval(-7200),
            expiresAt: Date().addingTimeInterval(48 * 3600), // 2 days
            videoURL: nil
        ),
        Video(
            id: UUID(),
            problem: "Prove by induction: 1 + 2 + ... + n = n(n+1)/2",
            category: "Discrete Math",
            subcategory: "Proofs",
            durationSeconds: 245,
            stepPreview: ["Base Case: Show true for n = 1", "Inductive Step: Assume true for n = k"],
            result: nil,
            createdAt: Date().addingTimeInterval(-86400),
            expiresAt: Date().addingTimeInterval(20 * 3600), // Less than 1 day - warning!
            videoURL: nil
        )
    ]
}
