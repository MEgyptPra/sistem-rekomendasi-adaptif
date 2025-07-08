def simple_recommendation(user, destinations):
    # Dummy logic: filter berdasarkan preferensi user
    prefs = user.preferences.split(",") if user and user.preferences else []
    result = []
    for d in destinations:
        if not prefs or d.category in prefs:
            result.append(d)
    return result