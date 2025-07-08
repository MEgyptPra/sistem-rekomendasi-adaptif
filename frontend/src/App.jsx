import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600">
      <h1 className="text-5xl font-bold text-white mb-2 drop-shadow-lg">
        Tailwind CSS Berhasil! 🎉
      </h1>
      <p className="text-xl text-white/80">
        Jika kamu melihat halaman ini berwarna <span className="font-semibold underline">gradasi biru-ungu</span> dan tulisan seperti ini, maka Tailwind CSS sudah aktif!
      </p>
      <button className="mt-8 px-6 py-2 bg-white text-blue-600 rounded-lg shadow hover:bg-blue-100 transition">
        Contoh Tombol Tailwind
      </button>
    </div>
  );
}


export default App
