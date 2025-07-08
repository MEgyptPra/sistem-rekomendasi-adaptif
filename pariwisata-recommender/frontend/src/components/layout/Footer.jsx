import { MapPin, Heart, Github } from 'lucide-react';

function Footer() {
  return (
    <footer className="bg-gray-50 border-t">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <MapPin className="h-6 w-6 text-blue-600" />
            <span className="text-lg font-semibold text-gray-900">Tourism Recommender</span>
          </div>

          <div className="flex items-center space-x-6">
            <a href="#" className="text-gray-600 hover:text-blue-600 text-sm">
              About
            </a>
            <a href="#" className="text-gray-600 hover:text-blue-600 text-sm">
              Contact
            </a>
            <a href="#" className="text-gray-600 hover:text-blue-600 text-sm">
              Privacy
            </a>
            <a href="#" className="text-gray-600 hover:text-blue-600">
              <Github className="h-5 w-5" />
            </a>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-gray-200 text-center">
          <p className="text-sm text-gray-600 flex items-center justify-center">
            Made with <Heart className="h-4 w-4 mx-1 text-red-500" /> for tourism recommendation
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;