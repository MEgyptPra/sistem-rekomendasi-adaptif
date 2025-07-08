import { User, Settings, Heart, MapPin, Star, Clock } from 'lucide-react';

function Profile() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Profile Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex items-center space-x-6">
            <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center">
              <User className="h-12 w-12 text-blue-600" />
            </div>
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900">John Doe</h1>
              <p className="text-gray-600">Travel Enthusiast</p>
              <p className="text-sm text-gray-500 mt-1">Member since January 2024</p>
            </div>
            <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              <Settings className="h-4 w-4" />
              <span>Edit Profile</span>
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Stats */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Travel Stats</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Destinations Visited</span>
                <span className="font-semibold text-blue-600">12</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Reviews Written</span>
                <span className="font-semibold text-blue-600">8</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Recommendations Used</span>
                <span className="font-semibold text-blue-600">24</span>
              </div>
            </div>
          </div>

          {/* Preferences */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Preferences</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Budget Range</span>
                <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">$$</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Travel Style</span>
                <span className="text-sm bg-green-100 text-green-800 px-2 py-1 rounded">Adventure</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Group Size</span>
                <span className="text-sm bg-purple-100 text-purple-800 px-2 py-1 rounded">Small</span>
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Heart className="h-4 w-4 text-red-500" />
                <span className="text-sm text-gray-600">Liked "Beach Resort"</span>
              </div>
              <div className="flex items-center space-x-3">
                <Star className="h-4 w-4 text-yellow-500" />
                <span className="text-sm text-gray-600">Rated "Mountain Trail"</span>
              </div>
              <div className="flex items-center space-x-3">
                <MapPin className="h-4 w-4 text-blue-500" />
                <span className="text-sm text-gray-600">Visited "City Center"</span>
              </div>
            </div>
          </div>
        </div>

        {/* Favorites */}
        <div className="bg-white rounded-lg shadow-sm p-6 mt-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Favorite Destinations</h2>
            <button className="text-blue-600 hover:text-blue-700 text-sm">View All</button>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3].map((item) => (
              <div key={item} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center">
                    <MapPin className="h-6 w-6 text-gray-500" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900">Favorite Place {item}</h3>
                    <p className="text-sm text-gray-600">Beautiful destination</p>
                  </div>
                  <Heart className="h-5 w-5 text-red-500" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;