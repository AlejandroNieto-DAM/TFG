//
//  RandomPhotoImage.swift
//  prueba5
//
//  Created by Alejandro Nieto Alarcon on 12/05/2020.
//  Copyright © 2020 Alejandro Nieto Alarcon. All rights reserved.
//

import Foundation

// MARK: - Welcome
class RandomPhotoImage: Codable {
    let id: String
    let createdAt, updatedAt, promotedAt: Date
    let width, height: Int
    let color: String
    let welcomeDescription: JSONNull?
    let altDescription: String
    let urls: Urls
    let links: WelcomeLinks
    let categories: [JSONAny]
    let likes: Int
    let likedByUser: Bool
    let currentUserCollections: [JSONAny]
    let sponsorship: JSONNull?
    let user: User
    let exif: Exif
    let location: Location
    let views, downloads: Int

    enum CodingKeys: String, CodingKey {
        case id
        case createdAt = "created_at"
        case updatedAt = "updated_at"
        case promotedAt = "promoted_at"
        case width, height, color
        case welcomeDescription = "description"
        case altDescription = "alt_description"
        case urls, links, categories, likes
        case likedByUser = "liked_by_user"
        case currentUserCollections = "current_user_collections"
        case sponsorship, user, exif, location, views, downloads
    }

    init(id: String, createdAt: Date, updatedAt: Date, promotedAt: Date, width: Int, height: Int, color: String, welcomeDescription: JSONNull?, altDescription: String, urls: Urls, links: WelcomeLinks, categories: [JSONAny], likes: Int, likedByUser: Bool, currentUserCollections: [JSONAny], sponsorship: JSONNull?, user: User, exif: Exif, location: Location, views: Int, downloads: Int) {
        self.id = id
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.promotedAt = promotedAt
        self.width = width
        self.height = height
        self.color = color
        self.welcomeDescription = welcomeDescription
        self.altDescription = altDescription
        self.urls = urls
        self.links = links
        self.categories = categories
        self.likes = likes
        self.likedByUser = likedByUser
        self.currentUserCollections = currentUserCollections
        self.sponsorship = sponsorship
        self.user = user
        self.exif = exif
        self.location = location
        self.views = views
        self.downloads = downloads
    }
    
    func getUrlPhoto() -> String {
        return self.urls.regular
    }
}

// MARK: - Exif
class Exif: Codable {
    let make, model, exposureTime, aperture: String
    let focalLength: String
    let iso: Int

    enum CodingKeys: String, CodingKey {
        case make, model
        case exposureTime = "exposure_time"
        case aperture
        case focalLength = "focal_length"
        case iso
    }

    init(make: String, model: String, exposureTime: String, aperture: String, focalLength: String, iso: Int) {
        self.make = make
        self.model = model
        self.exposureTime = exposureTime
        self.aperture = aperture
        self.focalLength = focalLength
        self.iso = iso
    }
}

// MARK: - WelcomeLinks
class WelcomeLinks: Codable {
    let linksSelf, html, download, downloadLocation: String

    enum CodingKeys: String, CodingKey {
        case linksSelf = "self"
        case html, download
        case downloadLocation = "download_location"
    }

    init(linksSelf: String, html: String, download: String, downloadLocation: String) {
        self.linksSelf = linksSelf
        self.html = html
        self.download = download
        self.downloadLocation = downloadLocation
    }
}

// MARK: - Location
class Location: Codable {
    let title, name, city, country: String
    let position: Position

    init(title: String, name: String, city: String, country: String, position: Position) {
        self.title = title
        self.name = name
        self.city = city
        self.country = country
        self.position = position
    }
}

// MARK: - Position
class Position: Codable {
    let latitude, longitude: Double

    init(latitude: Double, longitude: Double) {
        self.latitude = latitude
        self.longitude = longitude
    }
}

// MARK: - Urls
class Urls: Codable {
    let raw, full, regular, small: String
    let thumb: String

    init(raw: String, full: String, regular: String, small: String, thumb: String) {
        self.raw = raw
        self.full = full
        self.regular = regular
        self.small = small
        self.thumb = thumb
    }
}

// MARK: - User
class User: Codable {
    let id: String
    let updatedAt: Date
    let username, name, firstName, lastName: String
    let twitterUsername, portfolioURL: JSONNull?
    let bio, location: String
    let links: UserLinks
    let profileImage: ProfileImage
    let instagramUsername: String
    let totalCollections, totalLikes, totalPhotos: Int
    let acceptedTos: Bool

    enum CodingKeys: String, CodingKey {
        case id
        case updatedAt = "updated_at"
        case username, name
        case firstName = "first_name"
        case lastName = "last_name"
        case twitterUsername = "twitter_username"
        case portfolioURL = "portfolio_url"
        case bio, location, links
        case profileImage = "profile_image"
        case instagramUsername = "instagram_username"
        case totalCollections = "total_collections"
        case totalLikes = "total_likes"
        case totalPhotos = "total_photos"
        case acceptedTos = "accepted_tos"
    }

    init(id: String, updatedAt: Date, username: String, name: String, firstName: String, lastName: String, twitterUsername: JSONNull?, portfolioURL: JSONNull?, bio: String, location: String, links: UserLinks, profileImage: ProfileImage, instagramUsername: String, totalCollections: Int, totalLikes: Int, totalPhotos: Int, acceptedTos: Bool) {
        self.id = id
        self.updatedAt = updatedAt
        self.username = username
        self.name = name
        self.firstName = firstName
        self.lastName = lastName
        self.twitterUsername = twitterUsername
        self.portfolioURL = portfolioURL
        self.bio = bio
        self.location = location
        self.links = links
        self.profileImage = profileImage
        self.instagramUsername = instagramUsername
        self.totalCollections = totalCollections
        self.totalLikes = totalLikes
        self.totalPhotos = totalPhotos
        self.acceptedTos = acceptedTos
    }
}

// MARK: - UserLinks
class UserLinks: Codable {
    let linksSelf, html, photos, likes: String
    let portfolio, following, followers: String

    enum CodingKeys: String, CodingKey {
        case linksSelf = "self"
        case html, photos, likes, portfolio, following, followers
    }

    init(linksSelf: String, html: String, photos: String, likes: String, portfolio: String, following: String, followers: String) {
        self.linksSelf = linksSelf
        self.html = html
        self.photos = photos
        self.likes = likes
        self.portfolio = portfolio
        self.following = following
        self.followers = followers
    }
}

// MARK: - ProfileImage
class ProfileImage: Codable {
    let small, medium, large: String

    init(small: String, medium: String, large: String) {
        self.small = small
        self.medium = medium
        self.large = large
    }
}

// MARK: - Encode/decode helpers

class JSONNull: Codable, Hashable {

    public static func == (lhs: JSONNull, rhs: JSONNull) -> Bool {
        return true
    }

    public var hashValue: Int {
        return 0
    }

    public init() {}

    public required init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        if !container.decodeNil() {
            throw DecodingError.typeMismatch(JSONNull.self, DecodingError.Context(codingPath: decoder.codingPath, debugDescription: "Wrong type for JSONNull"))
        }
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        try container.encodeNil()
    }
}

class JSONCodingKey: CodingKey {
    let key: String

    required init?(intValue: Int) {
        return nil
    }

    required init?(stringValue: String) {
        key = stringValue
    }

    var intValue: Int? {
        return nil
    }

    var stringValue: String {
        return key
    }
}

class JSONAny: Codable {

    let value: Any

    static func decodingError(forCodingPath codingPath: [CodingKey]) -> DecodingError {
        let context = DecodingError.Context(codingPath: codingPath, debugDescription: "Cannot decode JSONAny")
        return DecodingError.typeMismatch(JSONAny.self, context)
    }

    static func encodingError(forValue value: Any, codingPath: [CodingKey]) -> EncodingError {
        let context = EncodingError.Context(codingPath: codingPath, debugDescription: "Cannot encode JSONAny")
        return EncodingError.invalidValue(value, context)
    }

    static func decode(from container: SingleValueDecodingContainer) throws -> Any {
        if let value = try? container.decode(Bool.self) {
            return value
        }
        if let value = try? container.decode(Int64.self) {
            return value
        }
        if let value = try? container.decode(Double.self) {
            return value
        }
        if let value = try? container.decode(String.self) {
            return value
        }
        if container.decodeNil() {
            return JSONNull()
        }
        throw decodingError(forCodingPath: container.codingPath)
    }

    static func decode(from container: inout UnkeyedDecodingContainer) throws -> Any {
        if let value = try? container.decode(Bool.self) {
            return value
        }
        if let value = try? container.decode(Int64.self) {
            return value
        }
        if let value = try? container.decode(Double.self) {
            return value
        }
        if let value = try? container.decode(String.self) {
            return value
        }
        if let value = try? container.decodeNil() {
            if value {
                return JSONNull()
            }
        }
        if var container = try? container.nestedUnkeyedContainer() {
            return try decodeArray(from: &container)
        }
        if var container = try? container.nestedContainer(keyedBy: JSONCodingKey.self) {
            return try decodeDictionary(from: &container)
        }
        throw decodingError(forCodingPath: container.codingPath)
    }

    static func decode(from container: inout KeyedDecodingContainer<JSONCodingKey>, forKey key: JSONCodingKey) throws -> Any {
        if let value = try? container.decode(Bool.self, forKey: key) {
            return value
        }
        if let value = try? container.decode(Int64.self, forKey: key) {
            return value
        }
        if let value = try? container.decode(Double.self, forKey: key) {
            return value
        }
        if let value = try? container.decode(String.self, forKey: key) {
            return value
        }
        if let value = try? container.decodeNil(forKey: key) {
            if value {
                return JSONNull()
            }
        }
        if var container = try? container.nestedUnkeyedContainer(forKey: key) {
            return try decodeArray(from: &container)
        }
        if var container = try? container.nestedContainer(keyedBy: JSONCodingKey.self, forKey: key) {
            return try decodeDictionary(from: &container)
        }
        throw decodingError(forCodingPath: container.codingPath)
    }

    static func decodeArray(from container: inout UnkeyedDecodingContainer) throws -> [Any] {
        var arr: [Any] = []
        while !container.isAtEnd {
            let value = try decode(from: &container)
            arr.append(value)
        }
        return arr
    }

    static func decodeDictionary(from container: inout KeyedDecodingContainer<JSONCodingKey>) throws -> [String: Any] {
        var dict = [String: Any]()
        for key in container.allKeys {
            let value = try decode(from: &container, forKey: key)
            dict[key.stringValue] = value
        }
        return dict
    }

    static func encode(to container: inout UnkeyedEncodingContainer, array: [Any]) throws {
        for value in array {
            if let value = value as? Bool {
                try container.encode(value)
            } else if let value = value as? Int64 {
                try container.encode(value)
            } else if let value = value as? Double {
                try container.encode(value)
            } else if let value = value as? String {
                try container.encode(value)
            } else if value is JSONNull {
                try container.encodeNil()
            } else if let value = value as? [Any] {
                var container = container.nestedUnkeyedContainer()
                try encode(to: &container, array: value)
            } else if let value = value as? [String: Any] {
                var container = container.nestedContainer(keyedBy: JSONCodingKey.self)
                try encode(to: &container, dictionary: value)
            } else {
                throw encodingError(forValue: value, codingPath: container.codingPath)
            }
        }
    }

    static func encode(to container: inout KeyedEncodingContainer<JSONCodingKey>, dictionary: [String: Any]) throws {
        for (key, value) in dictionary {
            let key = JSONCodingKey(stringValue: key)!
            if let value = value as? Bool {
                try container.encode(value, forKey: key)
            } else if let value = value as? Int64 {
                try container.encode(value, forKey: key)
            } else if let value = value as? Double {
                try container.encode(value, forKey: key)
            } else if let value = value as? String {
                try container.encode(value, forKey: key)
            } else if value is JSONNull {
                try container.encodeNil(forKey: key)
            } else if let value = value as? [Any] {
                var container = container.nestedUnkeyedContainer(forKey: key)
                try encode(to: &container, array: value)
            } else if let value = value as? [String: Any] {
                var container = container.nestedContainer(keyedBy: JSONCodingKey.self, forKey: key)
                try encode(to: &container, dictionary: value)
            } else {
                throw encodingError(forValue: value, codingPath: container.codingPath)
            }
        }
    }

    static func encode(to container: inout SingleValueEncodingContainer, value: Any) throws {
        if let value = value as? Bool {
            try container.encode(value)
        } else if let value = value as? Int64 {
            try container.encode(value)
        } else if let value = value as? Double {
            try container.encode(value)
        } else if let value = value as? String {
            try container.encode(value)
        } else if value is JSONNull {
            try container.encodeNil()
        } else {
            throw encodingError(forValue: value, codingPath: container.codingPath)
        }
    }

    public required init(from decoder: Decoder) throws {
        if var arrayContainer = try? decoder.unkeyedContainer() {
            self.value = try JSONAny.decodeArray(from: &arrayContainer)
        } else if var container = try? decoder.container(keyedBy: JSONCodingKey.self) {
            self.value = try JSONAny.decodeDictionary(from: &container)
        } else {
            let container = try decoder.singleValueContainer()
            self.value = try JSONAny.decode(from: container)
        }
    }

    public func encode(to encoder: Encoder) throws {
        if let arr = self.value as? [Any] {
            var container = encoder.unkeyedContainer()
            try JSONAny.encode(to: &container, array: arr)
        } else if let dict = self.value as? [String: Any] {
            var container = encoder.container(keyedBy: JSONCodingKey.self)
            try JSONAny.encode(to: &container, dictionary: dict)
        } else {
            var container = encoder.singleValueContainer()
            try JSONAny.encode(to: &container, value: self.value)
        }
    }
}
