import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { 
  BarChart3, 
  Users, 
  MapPin, 
  Star, 
  TrendingUp,
  Settings,
  Brain,
  RefreshCw
} from 'lucide-react';
import { destinationsAPI, recommendationsAPI } from '../services/api';

const Admin = () => {
  const [isTraining, setIsTraining] = useState(false);
  
  // Fetch analytics data
  const { data: destinationAnalytics } = useQuery(
    'destination-analytics',
    () => destinationsAPI.getAnalytics(),
    { select: (data) => data.data }
  );

  const handleTrainModels = async () => {
    setIsTraining(true);
    try {
      await recommendationsAPI.train();
      // Show success toast
    } catch (error) {
      // Show error toast
    } finally {
      setIsTraining(false);
    }
  };

  const stats = [
    {
      label: 'Total Destinasi',
      value: destinationAnalytics?.length || 0,
      icon: MapPin,
      color: 'blue'
    },
    {
      label: 'Total Rating',
      value: destinationAnalytics?.reduce((sum, d) => sum + d.rating_count, 0) || 0,
      icon: Star,
      color: 'yellow'
    },
    {
      label: 'Rata-rata Rating',
      value: destinationAnalytics?.reduce((sum, d) => sum + d.average_rating, 0) / (destinationAnalytics?.length || 1) || 0,
      icon: TrendingUp,
      color: 'green'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Dashboard Admin
          </h1>
          <p className="text-gray-600">
            Kelola sistem rekomendasi dan analitik
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className={`p-3 rounded-lg bg-${stat.color}-100`}>
                    <Icon className={`h-6 w-6 text-${stat.color}-600`} />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">
                      {stat.label}
                    </p>
                    <p className="text-2xl font-bold text-gray-900">
                      {typeof stat.value === 'number' ? stat.value.toFixed(1) : stat.value}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Actions */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Model Management
          </h2>
          <div className="flex space-x-4">
            <button
              onClick={handleTrainModels}
              disabled={isTraining}
              className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
            >
              {isTraining ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                <Brain className="h-4 w-4" />
              )}
              <span>{isTraining ? 'Training...' : 'Train Models'}</span>
            </button>
          </div>
        </div>

        {/* Analytics Table */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">
              Analitik Destinasi
            </h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Destinasi
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Jumlah Rating
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rata-rata Rating
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Range Rating
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {destinationAnalytics?.map((destination) => (
                  <tr key={destination.destination_id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-medium text-gray-900">
                        {destination.destination_name}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-900">
                      {destination.rating_count}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <Star className="h-4 w-4 text-yellow-400 fill-current mr-1" />
                        <span className="text-gray-900">
                          {destination.average_rating.toFixed(1)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-900">
                      {destination.min_rating} - {destination.max_rating}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Admin;