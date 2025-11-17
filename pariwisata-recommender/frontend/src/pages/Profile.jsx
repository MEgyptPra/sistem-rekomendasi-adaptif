export default function Profile() {
  const isLoggedIn = !!localStorage.getItem('access_token');
  return (
    <div>
      <h2>Profil Pengguna</h2>
      {/* ...info user lain... */}
      {isLoggedIn && (
        <a href="/profile/itinerary" className="btn primary">Lihat Itinerary Saya</a>
      )}
    </div>
  );
}