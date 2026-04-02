"""
Generate a dataset of unique voice search queries.
Output: voice_search_query_captures_multilingual.csv with one column: query_text
Target: ~1475 English + ~164 multilingual = ~1640 unique queries
"""

import csv
import random

random.seed(42)

# Templates for English query generation
# Each intent has templates with slots to fill, producing unique queries.

ENTERTAINMENT_TEMPLATES = [
    "Play {genre} music",
    "Play some {genre}",
    "Play {artist}",
    "Play the latest {artist} album",
    "Show me {genre} movies",
    "Show me {genre} movies on {platform}",
    "Find me a {genre} podcast",
    "Recommend a {genre} {media}",
    "What's trending on {platform}?",
    "What's new on {platform}?",
    "What are the best {genre} {media}s right now?",
    "Play {mood} music for {activity}",
    "Show me {media}s by {artist}",
    "What's the top {media} on {platform}?",
    "Find {genre} {media}s rated {rating}",
    "What time does the {event} start?",
    "Play an audiobook by {author}",
    "What are the {award} nominees this year?",
    "Show me upcoming {media} releases",
    "Play {media} trailers",
    "What games are on {day}?",
    "Show me viral videos {timeframe}",
    "What's the score of the {team} game?",
    "Find a good {genre} series",
    "Play {playlist_type} playlist",
    "Recommend a {media} for {occasion}",
    "Show me {genre} on YouTube",
    "Play the top {number} hits",
    "Stream {event} live",
    "Who stars in {movie}?",
]

NAVIGATION_TEMPLATES = [
    "How do I get to {place}?",
    "Directions to the nearest {place_type}",
    "Directions to {place}",
    "Find the nearest {place_type}",
    "Navigate to {place}",
    "Navigate to the nearest {place_type}",
    "Take me to {place}",
    "Take me to the nearest {place_type}",
    "Show me the fastest route to {place}",
    "Route to {place}",
    "How far is {place} from here?",
    "Find a {place_type} near me",
    "Where is the closest {place_type}?",
    "Show me {transport} directions to {place}",
    "How long to drive to {place}?",
    "Route avoiding {avoid}",
    "Find a {adj} {place_type} nearby",
    "Is there a {place_type} ahead?",
    "Show {traffic_info} on my commute",
    "How do I avoid the {road_type}?",
    "Find a {place_type} with {amenity}",
    "What's the best route to {place}?",
    "Show me {place_type}s near {place}",
    "How far is it to the next {place_type}?",
    "Find a scenic route to {place}",
]

SHOPPING_TEMPLATES = [
    "Order {item} from {store}",
    "Buy {item}",
    "Buy a new {item}",
    "Find deals on {item}",
    "Compare prices for {item}",
    "Track my {store} order",
    "Add {grocery} to my shopping list",
    "Add {grocery} to my cart",
    "Show me {adj} {item}",
    "Find the cheapest {item}",
    "Where can I buy {item} nearby?",
    "Show me today's deals on {store}",
    "Reorder my last {store} order",
    "Find a coupon for {store}",
    "How much does {item} cost?",
    "Order {food} for delivery",
    "Find the best deal on {item}",
    "Book {service} near me",
    "Buy tickets for {event}",
    "Show me {category} on sale",
    "Order a replacement {item}",
    "Find {adj} {item} under ${price}",
    "Buy a gift for {person}",
    "Find {service} nearby",
    "Order {item} online",
    "Show me reviews for {item}",
    "Compare {item_a} and {item_b}",
    "Restock {grocery}",
    "Find {holiday} deals",
    "Subscribe to {service}",
]

INFORMATION_TEMPLATES = [
    "What's the weather in {city}?",
    "What's the weather like {timeframe}?",
    "What time is it in {city}?",
    "How many {unit} in a {measure}?",
    "What is the capital of {country}?",
    "What's the {metric} of {subject}?",
    "How does {concept} work?",
    "Who {action} {subject}?",
    "When is {event}?",
    "When was {subject} {event_verb}?",
    "What does {term} stand for?",
    "What is {concept}?",
    "How {adjective} is {subject}?",
    "What are the symptoms of {condition}?",
    "Who is the {role} of {entity}?",
    "How far is {place_a} from {place_b}?",
    "What language do they speak in {country}?",
    "What is the meaning of {word}?",
    "How many {thing} are in {container}?",
    "What causes {phenomenon}?",
    "Define {term}",
    "Tell me about {subject}",
    "What's the {stat} of {entity}?",
    "How old is {subject}?",
    "What are {subject}?",
    "Who won the {event} last {time}?",
    "What's the difference between {a} and {b}?",
    "Is {subject} {adjective}?",
    "How do you say {word} in {language}?",
    "What's the origin of {subject}?",
]

COMMAND_TEMPLATES = [
    "Set an alarm for {time}",
    "Set a timer for {duration}",
    "Remind me to {task} at {time}",
    "Remind me about {event} {timeframe}",
    "Call {person}",
    "Send a text to {person}",
    "Send {person} a message saying {message}",
    "Turn {on_off} the {device}",
    "Turn {direction} the {setting}",
    "{action} the {device}",
    "Open {app}",
    "Pair my {device}",
    "Set the {setting} to {value}",
    "Cancel my {item}",
    "Schedule a {event} for {day}",
    "Switch to {mode} mode",
    "Enable {feature}",
    "Disable {feature}",
    "{action} all {items}",
    "Start {item}",
    "Stop {item}",
    "Add a calendar event for {event}",
    "Reply to {person}'s message",
    "Read my last {item}",
    "Check my {item}",
]

# ── Slot fillers ────────────────────────────────────────────────────────────

GENRES = [
    "jazz", "rock", "pop", "classical", "country", "hip hop", "R&B", "indie",
    "electronic", "metal", "folk", "blues", "reggae", "punk", "soul", "Latin",
    "lo-fi", "ambient", "K-pop", "Bollywood",
    "action", "comedy", "horror", "thriller", "romance", "sci-fi", "fantasy",
    "documentary", "mystery", "drama", "animated", "adventure", "crime",
    "true crime", "history", "science", "technology", "business", "sports",
    "cooking", "travel", "nature", "fitness", "self-help", "kids",
]

ARTISTS = [
    "Taylor Swift", "Drake", "The Beatles", "Adele", "Ed Sheeran", "BTS",
    "Beyoncé", "Coldplay", "Kendrick Lamar", "Bad Bunny", "The Weeknd",
    "Billie Eilish", "Harry Styles", "Dua Lipa", "Post Malone", "SZA",
    "Rihanna", "Eminem", "Ariana Grande", "Bruno Mars", "Travis Scott",
    "Olivia Rodrigo", "Doja Cat", "Morgan Wallen",
]

PLATFORMS = [
    "Netflix", "Spotify", "YouTube", "Hulu", "Disney Plus", "Amazon Prime",
    "HBO Max", "Apple Music", "Peacock", "Paramount Plus", "Tidal",
    "Apple TV", "Crunchyroll",
]

MEDIA_TYPES = ["movie", "show", "series", "podcast", "song", "album", "book", "documentary", "playlist"]
MOODS = ["relaxing", "upbeat", "chill", "energetic", "happy", "sad", "motivational", "calm", "intense"]
ACTIVITIES = ["studying", "working out", "cooking", "sleeping", "driving", "reading", "running", "yoga", "dinner", "cleaning"]
AUTHORS = [
    "Stephen King", "J.K. Rowling", "James Patterson", "Dan Brown", "Malcolm Gladwell",
    "Michelle Obama", "Yuval Harari", "Brené Brown", "Walter Isaacson", "Colleen Hoover",
]
AWARDS = ["Oscar", "Grammy", "Emmy", "Tony", "Golden Globe", "BAFTA"]
EVENTS_ENT = ["concert", "game", "match", "premiere", "show", "festival", "tournament"]
TEAMS = ["Lakers", "Yankees", "Warriors", "Patriots", "Chelsea", "Real Madrid", "Red Sox", "Celtics", "Chiefs", "Eagles"]
MOVIES = [
    "Inception", "The Batman", "Oppenheimer", "Barbie", "Dune", "Spider-Man",
    "Top Gun Maverick", "Avatar", "The Godfather", "Interstellar",
]
RATINGS = ["PG", "PG-13", "R", "G"]
DAYS = ["tonight", "today", "tomorrow", "this weekend", "Friday", "Saturday", "Sunday"]
NUMBERS = ["10", "20", "40", "50", "100"]
PLAYLIST_TYPES = ["workout", "road trip", "study", "party", "morning", "evening", "sleep", "focus", "random", "chill"]
OCCASIONS = ["tonight", "date night", "a rainy day", "the family", "the weekend", "kids"]
TIMEFRAMES = ["today", "this week", "right now", "tonight", "tomorrow"]

PLACES = [
    "Central Park", "the airport", "downtown", "the train station", "the mall",
    "the beach", "the museum", "the zoo", "the waterfront", "Times Square",
    "the convention center", "the stadium", "the university", "the marina",
    "the botanical garden", "the city center", "the ferry terminal", "the market",
    "home", "work", "school", "the office", "mom's house", "the gym",
    "the dentist", "the vet", "the hotel", "the church", "the park",
    "the courthouse", "Boston", "San Francisco", "Chicago", "Miami",
    "the hospital", "the community center",
]

PLACE_TYPES = [
    "gas station", "coffee shop", "restaurant", "pharmacy", "hospital",
    "ATM", "parking spot", "hotel", "library", "dog park", "Starbucks",
    "grocery store", "post office", "urgent care", "subway station",
    "fire station", "hardware store", "pet store", "laundromat", "bank",
    "dentist", "barber shop", "car wash", "gym", "movie theater",
    "bookstore", "florist", "dry cleaner", "bike shop", "auto repair shop",
    "EV charger", "rest stop",
]

TRANSPORTS = ["walking", "biking", "driving", "transit", "bus"]
AVOIDS = ["tolls", "highways", "traffic", "construction", "ferries"]
PLACE_ADJS = ["24-hour", "open", "cheap", "good", "highly rated", "kid-friendly", "pet-friendly"]
TRAFFIC_INFO = ["traffic", "road conditions", "accidents", "construction delays"]
ROAD_TYPES = ["highway", "freeway", "toll road", "interstate", "bridge"]
AMENITIES = ["a car wash", "free air", "EV charging", "restrooms", "a drive-through", "Wi-Fi"]

ITEMS = [
    "headphones", "laptop", "phone case", "sneakers", "sunglasses", "backpack",
    "water bottle", "keyboard", "monitor", "tablet", "smartwatch", "camera",
    "drone", "speaker", "desk lamp", "office chair", "gaming mouse",
    "yoga mat", "running shoes", "winter jacket", "suitcase", "mattress",
    "coffee machine", "blender", "air purifier", "robot vacuum", "printer",
    "bicycle", "skateboard", "tent", "sleeping bag", "hiking boots",
    "rain jacket", "umbrella", "portable charger", "wireless earbuds",
    "fitness tracker", "electric toothbrush", "hair dryer", "iron",
    "contact lenses", "vitamins", "protein powder", "resistance bands",
]

STORES = ["Amazon", "Walmart", "Target", "Best Buy", "Costco", "Whole Foods", "DoorDash", "Uber Eats", "Instacart"]
GROCERIES = [
    "milk", "eggs", "bread", "butter", "cheese", "bananas", "apples", "chicken",
    "rice", "pasta", "tomatoes", "onions", "potatoes", "lettuce", "yogurt",
    "orange juice", "cereal", "coffee", "tea", "sugar", "flour", "olive oil",
    "avocados", "salmon", "ground beef", "tortillas", "salsa", "ice cream",
    "frozen pizza", "paper towels", "dish soap", "laundry detergent", "trash bags",
    "batteries", "dog food", "cat food", "baby formula", "diapers", "sunscreen",
]

ITEM_ADJS = ["best", "cheapest", "top-rated", "newest", "refurbished", "wireless", "portable", "waterproof"]
FOODS = ["pizza", "sushi", "Thai food", "Chinese food", "tacos", "burgers", "Indian food", "ramen", "salad", "sandwiches"]
SERVICES = ["a plumber", "an electrician", "a pet sitter", "a tutor", "a cleaner", "a mechanic", "a locksmith", "a photographer"]
CATEGORIES = ["electronics", "furniture", "clothing", "shoes", "kitchen appliances", "toys", "books", "home decor"]
PERSONS_SHOP = ["my sister", "my mom", "my dad", "my friend", "my partner", "the kids"]
HOLIDAYS = ["Black Friday", "Cyber Monday", "Christmas", "Prime Day", "back-to-school", "Valentine's Day"]
ITEM_PAIRS = [
    ("Samsung", "Apple watches"), ("Nike", "Adidas shoes"), ("iPad", "Surface tablet"),
    ("AirPods", "Galaxy Buds"), ("Kindle", "Nook"), ("MacBook", "ThinkPad"),
]
PRICES = ["50", "100", "200", "500"]

CITIES = [
    "Tokyo", "London", "Paris", "Sydney", "Dubai", "New York", "Berlin",
    "Mumbai", "Seoul", "Toronto", "Rome", "Bangkok", "Istanbul", "Moscow",
    "Cairo", "São Paulo", "Mexico City", "Jakarta", "Lagos", "Nairobi",
]

COUNTRIES = [
    "Australia", "Brazil", "Japan", "Germany", "France", "India", "Canada",
    "South Korea", "Mexico", "Egypt", "Nigeria", "Thailand", "Italy",
    "Turkey", "Indonesia", "Spain", "Sweden", "Norway", "Switzerland",
    "Argentina", "Chile", "Portugal", "Kenya", "Morocco", "Vietnam",
]

CONCEPTS = [
    "photosynthesis", "gravity", "inflation", "blockchain", "quantum computing",
    "machine learning", "climate change", "evolution", "DNA", "cryptocurrency",
    "dark matter", "the stock market", "nuclear fusion", "the water cycle",
    "compound interest", "natural selection", "plate tectonics", "relativity",
    "supply and demand", "entropy", "the greenhouse effect",
    "electric cars", "solar panels", "vaccines", "antibiotics",
    "3D printing", "gene editing", "cloud computing", "virtual reality",
    "autonomous driving",
]

SUBJECTS_INFO = [
    "the Eiffel Tower", "the Great Wall of China", "the Mariana Trench",
    "the Great Barrier Reef", "Mount Everest", "the Amazon River",
    "the Sahara Desert", "the Grand Canyon", "Niagara Falls",
    "the Pyramids of Giza", "the Colosseum", "the Statue of Liberty",
    "the Taj Mahal", "Machu Picchu", "Stonehenge",
    "the human body", "the solar system", "the internet",
    "the Declaration of Independence", "the Constitution",
    "the Olympic Games", "the World Cup", "the Super Bowl",
    "the Nobel Prize", "NASA", "the United Nations",
]

TERMS = [
    "GDP", "DNA", "NASA", "FAQ", "CEO", "AI", "IoT", "API", "VPN", "SaaS",
    "STEM", "MRI", "SEO", "ROI", "ETF", "RSVP", "ASAP", "UNESCO",
]

WORDS_MEANING = [
    "serendipity", "ephemeral", "ubiquitous", "pragmatic", "altruistic",
    "juxtaposition", "paradigm", "eloquent", "resilience", "empathy",
    "ambiguous", "cognizant", "meticulous", "gregarious", "tenacious",
]

CONDITIONS = [
    "the flu", "diabetes", "asthma", "allergies", "a migraine",
    "strep throat", "food poisoning", "dehydration", "insomnia",
    "anxiety", "high blood pressure", "a concussion", "pink eye",
    "carpal tunnel", "vertigo", "anemia", "sleep apnea",
]

ROLES = ["president", "prime minister", "CEO", "founder", "capital", "population", "king", "queen"]
ENTITIES = [
    "France", "Apple", "Google", "Tesla", "Amazon", "Microsoft",
    "Japan", "Brazil", "SpaceX", "the UK", "Canada", "South Korea", "Germany",
]

PHENOMENA = [
    "earthquakes", "tornadoes", "the Northern Lights", "tides", "rainbows",
    "thunder", "lightning", "fog", "frost", "avalanches", "tsunamis",
    "volcanic eruptions", "sinkholes", "droughts", "floods",
]

LANGUAGES_INFO = ["Spanish", "French", "Japanese", "Mandarin", "German", "Korean", "Italian", "Portuguese", "Arabic", "Hindi"]
WORDS_TRANSLATE = ["hello", "thank you", "goodbye", "please", "sorry", "water", "food", "help", "love", "beautiful"]

EVENTS_INFO = [
    "the next solar eclipse", "Thanksgiving this year", "daylight saving time",
    "the next World Cup", "the next Olympics", "Earth Day",
    "the next presidential election", "New Year's Eve", "the spring equinox",
    "the next meteor shower", "the midterm elections",
]

STATS = ["stock price", "population", "GDP", "area", "height", "distance", "age", "net worth"]

DIFF_PAIRS = [
    ("weather", "climate"), ("virus", "bacteria"), ("RAM", "ROM"),
    ("AC", "DC"), ("affect", "effect"), ("further", "farther"),
    ("empathy", "sympathy"), ("alligator", "crocodile"),
    ("asteroid", "comet"), ("ocean", "sea"),
]

# Command slot fillers
TIMES = ["6 AM", "6:30 AM", "7 AM", "7:30 AM", "8 AM", "9 AM", "10 AM", "noon", "1 PM", "3 PM", "5 PM", "6 PM", "8 PM", "10 PM"]
DURATIONS = ["5 minutes", "10 minutes", "15 minutes", "20 minutes", "30 minutes", "45 minutes", "1 hour", "2 hours", "90 seconds"]
TASKS = [
    "take my medicine", "call the dentist", "pick up the kids", "water the plants",
    "check the oven", "submit the report", "buy groceries", "feed the cat",
    "take out the trash", "renew my license", "pay the bills", "walk the dog",
    "do laundry", "book the flight", "send the email", "charge my phone",
    "stretch", "drink water", "eat lunch", "check in online",
]
PERSONS_CMD = ["Mom", "Dad", "John", "Sarah", "Mike", "Emily", "Alex", "the office", "my boss", "my doctor", "the restaurant"]
DEVICES = [
    "lights", "TV", "air conditioning", "heater", "fan", "oven", "microphone",
    "sprinklers", "fireplace", "garage door", "front door", "bedroom lights",
    "kitchen lights", "living room lights", "porch light",
]
APPS = [
    "Spotify", "Google Maps", "the camera", "Instagram", "WhatsApp", "the calculator",
    "the calendar", "my email", "the weather app", "Notes", "Settings",
    "the flashlight", "YouTube", "TikTok", "the banking app",
    "Uber", "the fitness app", "Slack", "Zoom", "Chrome",
]
SETTINGS_CMD = ["thermostat", "volume", "brightness", "bass", "timer"]
VALUES = ["72 degrees", "68 degrees", "75 degrees", "50%", "80%", "maximum", "minimum"]
MODES = ["dark", "silent", "airplane", "driving", "night", "power saving", "focus"]
FEATURES = ["Wi-Fi", "Bluetooth", "location services", "NFC", "mobile data", "auto-rotate", "Do Not Disturb"]
ON_OFF = ["on", "off"]
DIRECTIONS = ["up", "down"]
ACTIONS_CMD = ["Open", "Close", "Lock", "Unlock", "Start", "Stop", "Pause", "Resume"]
ITEMS_CMD = ["alarm", "timer", "reminder", "notifications", "apps", "tabs"]
EVENTS_CMD = ["meeting", "appointment", "call", "workout", "dinner", "study session"]
CMD_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "tomorrow", "next week"]
MESSAGES = ["I'm on my way", "I'll be late", "call me back", "see you soon", "running 10 minutes late"]
CHECK_ITEMS = ["battery level", "storage", "voicemail", "emails", "notifications", "schedule", "steps today"]
READ_ITEMS = ["email", "text message", "notification", "voicemail"]


def fill_entertainment():
    """Generate unique entertainment queries."""
    queries = set()
    for tmpl in ENTERTAINMENT_TEMPLATES:
        if "{genre}" in tmpl and "{platform}" in tmpl:
            for g in random.sample(GENRES, min(6, len(GENRES))):
                for p in random.sample(PLATFORMS, min(3, len(PLATFORMS))):
                    q = tmpl.format(genre=g, platform=p, media=random.choice(MEDIA_TYPES))
                    queries.add(q)
        elif "{genre}" in tmpl and "{media}" in tmpl:
            for g in random.sample(GENRES, min(8, len(GENRES))):
                m = random.choice(MEDIA_TYPES)
                q = tmpl.format(genre=g, media=m, rating=random.choice(RATINGS),
                                number=random.choice(NUMBERS))
                queries.add(q)
        elif "{artist}" in tmpl:
            for a in random.sample(ARTISTS, min(8, len(ARTISTS))):
                q = tmpl.format(artist=a, media=random.choice(MEDIA_TYPES))
                queries.add(q)
        elif "{platform}" in tmpl:
            for p in PLATFORMS:
                q = tmpl.format(platform=p, media=random.choice(MEDIA_TYPES))
                queries.add(q)
        elif "{mood}" in tmpl and "{activity}" in tmpl:
            for mood in random.sample(MOODS, min(5, len(MOODS))):
                for act in random.sample(ACTIVITIES, min(3, len(ACTIVITIES))):
                    queries.add(tmpl.format(mood=mood, activity=act))
        elif "{author}" in tmpl:
            for a in AUTHORS:
                queries.add(tmpl.format(author=a))
        elif "{award}" in tmpl:
            for a in AWARDS:
                queries.add(tmpl.format(award=a))
        elif "{team}" in tmpl:
            for t in TEAMS:
                queries.add(tmpl.format(team=t))
        elif "{movie}" in tmpl:
            for m in MOVIES:
                queries.add(tmpl.format(movie=m))
        elif "{event}" in tmpl:
            for e in EVENTS_ENT:
                queries.add(tmpl.format(event=e))
        elif "{day}" in tmpl:
            for d in DAYS:
                queries.add(tmpl.format(day=d))
        elif "{timeframe}" in tmpl:
            for t in TIMEFRAMES:
                queries.add(tmpl.format(timeframe=t))
        elif "{playlist_type}" in tmpl:
            for p in PLAYLIST_TYPES:
                queries.add(tmpl.format(playlist_type=p))
        elif "{occasion}" in tmpl:
            for o in OCCASIONS:
                queries.add(tmpl.format(occasion=o, media=random.choice(MEDIA_TYPES)))
        elif "{number}" in tmpl:
            for n in NUMBERS:
                queries.add(tmpl.format(number=n))
        else:
            queries.add(tmpl.replace("{media}", random.choice(MEDIA_TYPES)))
    return queries


def fill_navigation():
    queries = set()
    for tmpl in NAVIGATION_TEMPLATES:
        if "{place_type}" in tmpl and "{place}" in tmpl:
            for pt in random.sample(PLACE_TYPES, min(4, len(PLACE_TYPES))):
                for p in random.sample(PLACES, min(3, len(PLACES))):
                    queries.add(tmpl.format(place_type=pt, place=p))
        elif "{place}" in tmpl and "{transport}" in tmpl:
            for p in random.sample(PLACES, min(6, len(PLACES))):
                for t in random.sample(TRANSPORTS, min(2, len(TRANSPORTS))):
                    queries.add(tmpl.format(place=p, transport=t))
        elif "{place}" in tmpl:
            for p in PLACES:
                queries.add(tmpl.format(place=p, avoid=random.choice(AVOIDS),
                                        adj=random.choice(PLACE_ADJS),
                                        place_type=random.choice(PLACE_TYPES),
                                        transport=random.choice(TRANSPORTS)))
        elif "{place_type}" in tmpl and "{amenity}" in tmpl:
            for pt in random.sample(PLACE_TYPES, min(6, len(PLACE_TYPES))):
                for a in random.sample(AMENITIES, min(2, len(AMENITIES))):
                    queries.add(tmpl.format(place_type=pt, amenity=a))
        elif "{place_type}" in tmpl and "{adj}" in tmpl:
            for pt in random.sample(PLACE_TYPES, min(8, len(PLACE_TYPES))):
                for a in random.sample(PLACE_ADJS, min(2, len(PLACE_ADJS))):
                    queries.add(tmpl.format(place_type=pt, adj=a))
        elif "{place_type}" in tmpl:
            for pt in PLACE_TYPES:
                queries.add(tmpl.format(place_type=pt))
        elif "{avoid}" in tmpl:
            for a in AVOIDS:
                queries.add(tmpl.format(avoid=a))
        elif "{traffic_info}" in tmpl:
            for t in TRAFFIC_INFO:
                queries.add(tmpl.format(traffic_info=t))
        elif "{road_type}" in tmpl:
            for r in ROAD_TYPES:
                queries.add(tmpl.format(road_type=r))
    return queries


def fill_shopping():
    queries = set()
    for tmpl in SHOPPING_TEMPLATES:
        if "{item}" in tmpl and "{store}" in tmpl:
            for i in random.sample(ITEMS, min(4, len(ITEMS))):
                for s in random.sample(STORES, min(2, len(STORES))):
                    queries.add(tmpl.format(item=i, store=s, adj=random.choice(ITEM_ADJS)))
        elif "{grocery}" in tmpl:
            for g in GROCERIES:
                queries.add(tmpl.format(grocery=g))
        elif "{item}" in tmpl and "{adj}" in tmpl:
            for i in random.sample(ITEMS, min(8, len(ITEMS))):
                for a in random.sample(ITEM_ADJS, min(2, len(ITEM_ADJS))):
                    queries.add(tmpl.format(item=i, adj=a, price=random.choice(PRICES)))
        elif "{item_a}" in tmpl and "{item_b}" in tmpl:
            for a, b in ITEM_PAIRS:
                queries.add(tmpl.format(item_a=a, item_b=b))
        elif "{item}" in tmpl:
            for i in ITEMS:
                queries.add(tmpl.format(item=i, adj=random.choice(ITEM_ADJS),
                                        store=random.choice(STORES),
                                        price=random.choice(PRICES)))
        elif "{store}" in tmpl:
            for s in STORES:
                queries.add(tmpl.format(store=s))
        elif "{food}" in tmpl:
            for f in FOODS:
                queries.add(tmpl.format(food=f))
        elif "{service}" in tmpl:
            for s in SERVICES:
                queries.add(tmpl.format(service=s))
        elif "{event}" in tmpl:
            for e in EVENTS_ENT:
                queries.add(tmpl.format(event=e))
        elif "{category}" in tmpl:
            for c in CATEGORIES:
                queries.add(tmpl.format(category=c))
        elif "{person}" in tmpl:
            for p in PERSONS_SHOP:
                queries.add(tmpl.format(person=p))
        elif "{holiday}" in tmpl:
            for h in HOLIDAYS:
                queries.add(tmpl.format(holiday=h))
    return queries


def fill_information():
    queries = set()
    for tmpl in INFORMATION_TEMPLATES:
        if "{city}" in tmpl:
            for c in CITIES:
                queries.add(tmpl.format(city=c, timeframe=random.choice(TIMEFRAMES)))
        elif "{country}" in tmpl and "{language}" not in tmpl:
            for c in COUNTRIES:
                queries.add(tmpl.format(country=c))
        elif "{concept}" in tmpl:
            for c in CONCEPTS:
                queries.add(tmpl.format(concept=c))
        elif "{subject}" in tmpl and "{event_verb}" in tmpl:
            for s in random.sample(SUBJECTS_INFO, min(10, len(SUBJECTS_INFO))):
                queries.add(tmpl.format(subject=s, event_verb="created"))
                queries.add(tmpl.format(subject=s, event_verb="built"))
        elif "{subject}" in tmpl and "{adjective}" in tmpl:
            for s in random.sample(SUBJECTS_INFO, min(10, len(SUBJECTS_INFO))):
                queries.add(tmpl.format(subject=s, adjective=random.choice(["tall", "old", "deep", "long", "wide"])))
        elif "{subject}" in tmpl and "{action}" in tmpl:
            for s in random.sample(SUBJECTS_INFO, min(8, len(SUBJECTS_INFO))):
                queries.add(tmpl.format(subject=s, action=random.choice(["invented", "discovered", "built", "wrote", "founded"])))
        elif "{subject}" in tmpl:
            for s in SUBJECTS_INFO:
                queries.add(tmpl.format(subject=s, metric=random.choice(STATS),
                                        stat=random.choice(STATS)))
        elif "{term}" in tmpl:
            for t in TERMS:
                queries.add(tmpl.format(term=t))
        elif "{word}" in tmpl and "{language}" in tmpl:
            for w in random.sample(WORDS_TRANSLATE, min(5, len(WORDS_TRANSLATE))):
                for l in random.sample(LANGUAGES_INFO, min(3, len(LANGUAGES_INFO))):
                    queries.add(tmpl.format(word=w, language=l))
        elif "{word}" in tmpl:
            for w in WORDS_MEANING:
                queries.add(tmpl.format(word=w))
        elif "{event}" in tmpl and "{time}" in tmpl:
            for e in EVENTS_INFO:
                queries.add(tmpl.format(event=e, time=random.choice(["year", "season", "month"])))
        elif "{event}" in tmpl:
            for e in EVENTS_INFO:
                queries.add(tmpl.format(event=e))
        elif "{condition}" in tmpl:
            for c in CONDITIONS:
                queries.add(tmpl.format(condition=c))
        elif "{role}" in tmpl and "{entity}" in tmpl:
            for r in random.sample(ROLES, min(3, len(ROLES))):
                for e in random.sample(ENTITIES, min(4, len(ENTITIES))):
                    queries.add(tmpl.format(role=r, entity=e))
        elif "{place_a}" in tmpl and "{place_b}" in tmpl:
            pairs = [(a, b) for a in random.sample(CITIES, 5) for b in random.sample(CITIES, 3) if a != b]
            for a, b in pairs[:10]:
                queries.add(tmpl.format(place_a=a, place_b=b))
        elif "{a}" in tmpl and "{b}" in tmpl:
            for a, b in DIFF_PAIRS:
                queries.add(tmpl.format(a=a, b=b))
        elif "{phenomenon}" in tmpl:
            for p in PHENOMENA:
                queries.add(tmpl.format(phenomenon=p))
        elif "{unit}" in tmpl:
            pairs = [("calories", "banana"), ("ounces", "cup"), ("miles", "marathon"),
                     ("teaspoons", "tablespoon"), ("feet", "mile"), ("grams", "ounce")]
            for u, m in pairs:
                queries.add(tmpl.format(unit=u, measure=m))
        elif "{metric}" in tmpl:
            for s in random.sample(SUBJECTS_INFO, min(8, len(SUBJECTS_INFO))):
                queries.add(tmpl.format(metric=random.choice(STATS), subject=s))
        elif "{thing}" in tmpl:
            pairs = [("bones", "the human body"), ("states", "the US"), ("planets", "the solar system"),
                     ("continents", "the world"), ("teeth", "an adult mouth")]
            for t, c in pairs:
                queries.add(tmpl.format(thing=t, container=c))
    return queries


def fill_command():
    queries = set()
    for tmpl in COMMAND_TEMPLATES:
        if "{task}" in tmpl and "{time}" in tmpl:
            for task in random.sample(TASKS, min(8, len(TASKS))):
                for t in random.sample(TIMES, min(2, len(TIMES))):
                    queries.add(tmpl.format(task=task, time=t))
        elif "{event}" in tmpl and "{day}" in tmpl:
            for e in random.sample(EVENTS_CMD, min(4, len(EVENTS_CMD))):
                for d in random.sample(CMD_DAYS, min(3, len(CMD_DAYS))):
                    queries.add(tmpl.format(event=e, day=d))
        elif "{event}" in tmpl and "{timeframe}" in tmpl:
            for e in random.sample(EVENTS_CMD, min(4, len(EVENTS_CMD))):
                for t in random.sample(["tomorrow", "in an hour", "at 3 PM", "this evening"], 3):
                    queries.add(tmpl.format(event=e, timeframe=t))
        elif "{person}" in tmpl and "{message}" in tmpl:
            for p in random.sample(PERSONS_CMD, min(4, len(PERSONS_CMD))):
                for m in random.sample(MESSAGES, min(2, len(MESSAGES))):
                    queries.add(tmpl.format(person=p, message=m))
        elif "{person}" in tmpl:
            for p in PERSONS_CMD:
                queries.add(tmpl.format(person=p))
        elif "{on_off}" in tmpl and "{device}" in tmpl:
            for o in ON_OFF:
                for d in DEVICES:
                    queries.add(tmpl.format(on_off=o, device=d))
        elif "{direction}" in tmpl and "{setting}" in tmpl:
            for d in DIRECTIONS:
                for s in SETTINGS_CMD:
                    queries.add(tmpl.format(direction=d, setting=s))
        elif "{action}" in tmpl and "{device}" in tmpl:
            for a in random.sample(ACTIONS_CMD, min(3, len(ACTIONS_CMD))):
                for d in random.sample(DEVICES, min(5, len(DEVICES))):
                    queries.add(tmpl.format(action=a, device=d))
        elif "{app}" in tmpl:
            for a in APPS:
                queries.add(tmpl.format(app=a))
        elif "{setting}" in tmpl and "{value}" in tmpl:
            for s in SETTINGS_CMD:
                for v in random.sample(VALUES, min(2, len(VALUES))):
                    queries.add(tmpl.format(setting=s, value=v))
        elif "{mode}" in tmpl:
            for m in MODES:
                queries.add(tmpl.format(mode=m))
        elif "{feature}" in tmpl:
            for f in FEATURES:
                queries.add(tmpl.format(feature=f))
        elif "{time}" in tmpl:
            for t in TIMES:
                queries.add(tmpl.format(time=t))
        elif "{duration}" in tmpl:
            for d in DURATIONS:
                queries.add(tmpl.format(duration=d))
        elif "{item}" in tmpl and "{items}" not in tmpl:
            for i in random.sample(ITEMS_CMD + CHECK_ITEMS + READ_ITEMS, min(6, len(ITEMS_CMD))):
                queries.add(tmpl.format(item=i))
        elif "{items}" in tmpl:
            for i in ["notifications", "alarms", "tabs", "apps", "reminders"]:
                queries.add(tmpl.format(action=random.choice(["Clear", "Close", "Delete"]), items=i))
    return queries


# ── Multilingual queries ────────────────────────────────────────────────────

MULTILINGUAL_QUERIES = [
    # Spanish - Entertainment
    ("Pon mi canción favorita", "Spanish", "entertainment"),
    ("Muéstrame comedias en Netflix", "Spanish", "entertainment"),
    ("Recomiéndame un podcast de tecnología", "Spanish", "entertainment"),
    ("Reproduce los últimos tráilers de películas", "Spanish", "entertainment"),
    ("¿Qué series están de moda?", "Spanish", "entertainment"),
    # Spanish - Navigation
    ("Llévame al aeropuerto", "Spanish", "navigation"),
    ("¿Cómo llego al centro comercial?", "Spanish", "navigation"),
    ("Busca la gasolinera más cercana", "Spanish", "navigation"),
    ("Ruta a casa", "Spanish", "navigation"),
    ("Navegar a la estación de tren", "Spanish", "navigation"),
    # Spanish - Shopping
    ("Compra auriculares nuevos", "Spanish", "shopping"),
    ("Pide una pizza para mí", "Spanish", "shopping"),
    ("Rastrea mi pedido de Amazon", "Spanish", "shopping"),
    ("Busca tiendas de ropa cercanas", "Spanish", "shopping"),
    ("Agrega leche a la lista de compras", "Spanish", "shopping"),
    # Spanish - Information
    ("¿Cuál es el clima de hoy?", "Spanish", "information"),
    ("¿Quién ganó el partido anoche?", "Spanish", "information"),
    ("¿Qué altura tiene la Torre Eiffel?", "Spanish", "information"),
    ("Dime las noticias del día", "Spanish", "information"),
    ("Define inteligencia artificial", "Spanish", "information"),
    # Spanish - Command
    ("Pon una alarma a las siete", "Spanish", "command"),
    ("Abre el calendario", "Spanish", "command"),
    ("Apaga las luces", "Spanish", "command"),
    ("Llama a mamá", "Spanish", "command"),

    # French - Entertainment
    ("Joue ma chanson préférée", "French", "entertainment"),
    ("Montre-moi des comédies", "French", "entertainment"),
    ("Recommande-moi un podcast", "French", "entertainment"),
    ("Qu'est-ce qui est tendance sur Netflix?", "French", "entertainment"),
    ("Joue les dernières bandes-annonces", "French", "entertainment"),
    # French - Navigation
    ("Emmène-moi à l'aéroport", "French", "navigation"),
    ("Comment aller à Central Park?", "French", "navigation"),
    ("Trouve le café le plus proche", "French", "navigation"),
    ("Itinéraire vers la maison", "French", "navigation"),
    ("Direction la station-service la plus proche", "French", "navigation"),
    # French - Shopping
    ("Achète des écouteurs neufs", "French", "shopping"),
    ("Commande-moi une pizza", "French", "shopping"),
    ("Suis mon colis Amazon", "French", "shopping"),
    ("Trouve des magasins de vêtements proches", "French", "shopping"),
    ("Ajoute du lait à la liste de courses", "French", "shopping"),
    # French - Information
    ("Quel temps fait-il aujourd'hui?", "French", "information"),
    ("Qui a gagné le match hier soir?", "French", "information"),
    ("Quelle est la hauteur de la Tour Eiffel?", "French", "information"),
    ("Donne-moi les titres des actualités", "French", "information"),
    ("Définis l'intelligence artificielle", "French", "information"),
    # French - Command
    ("Mets une alarme à sept heures", "French", "command"),
    ("Ouvre le calendrier", "French", "command"),
    ("Éteins les lumières", "French", "command"),
    ("Appelle maman", "French", "command"),

    # Hindi - Entertainment
    ("मेरा पसंदीदा गाना बजाओ", "Hindi", "entertainment"),
    ("नेटफ्लिक्स पर क्या ट्रेंड कर रहा है?", "Hindi", "entertainment"),
    ("मुझे एक पॉडकास्ट सुझाओ", "Hindi", "entertainment"),
    ("कॉमेडी शो दिखाओ", "Hindi", "entertainment"),
    ("नई फिल्मों के ट्रेलर दिखाओ", "Hindi", "entertainment"),
    # Hindi - Navigation
    ("मुझे एयरपोर्ट ले चलो", "Hindi", "navigation"),
    ("सेंट्रल पार्क कैसे जाएं?", "Hindi", "navigation"),
    ("सबसे नज़दीकी कॉफी शॉप ढूंढो", "Hindi", "navigation"),
    ("घर का रास्ता बताओ", "Hindi", "navigation"),
    ("नज़दीकी पेट्रोल पंप खोजो", "Hindi", "navigation"),
    # Hindi - Shopping
    ("नए हेडफोन खरीदो", "Hindi", "shopping"),
    ("मेरे लिए पिज़्ज़ा ऑर्डर करो", "Hindi", "shopping"),
    ("मेरा अमेज़न ऑर्डर ट्रैक करो", "Hindi", "shopping"),
    ("पास की कपड़ों की दुकानें खोजो", "Hindi", "shopping"),
    ("शॉपिंग लिस्ट में दूध जोड़ो", "Hindi", "shopping"),
    # Hindi - Information
    ("आज मौसम कैसा है?", "Hindi", "information"),
    ("कल रात का मैच किसने जीता?", "Hindi", "information"),
    ("एफिल टावर कितना ऊंचा है?", "Hindi", "information"),
    ("आज की ताज़ा खबरें सुनाओ", "Hindi", "information"),
    ("कृत्रिम बुद्धिमत्ता की परिभाषा बताओ", "Hindi", "information"),
    # Hindi - Command
    ("सुबह सात बजे का अलार्म लगाओ", "Hindi", "command"),
    ("कैलेंडर खोलो", "Hindi", "command"),
    ("लाइट बंद करो", "Hindi", "command"),
    ("मम्मी को फोन लगाओ", "Hindi", "command"),

    # Mandarin - Entertainment
    ("播放我喜欢的歌", "Mandarin", "entertainment"),
    ("Netflix上有什么热门的?", "Mandarin", "entertainment"),
    ("给我推荐一个播客", "Mandarin", "entertainment"),
    ("播放最新电影预告片", "Mandarin", "entertainment"),
    ("有什么好看的喜剧节目?", "Mandarin", "entertainment"),
    # Mandarin - Navigation
    ("带我去机场", "Mandarin", "navigation"),
    ("怎么去中央公园?", "Mandarin", "navigation"),
    ("找最近的咖啡店", "Mandarin", "navigation"),
    ("导航回家", "Mandarin", "navigation"),
    ("最近的加油站在哪里?", "Mandarin", "navigation"),
    # Mandarin - Shopping
    ("买一副新耳机", "Mandarin", "shopping"),
    ("帮我点一个披萨", "Mandarin", "shopping"),
    ("追踪我的亚马逊订单", "Mandarin", "shopping"),
    ("找附近的服装店", "Mandarin", "shopping"),
    ("把牛奶加到购物清单", "Mandarin", "shopping"),
    # Mandarin - Information
    ("今天天气怎么样?", "Mandarin", "information"),
    ("昨晚比赛谁赢了?", "Mandarin", "information"),
    ("埃菲尔铁塔有多高?", "Mandarin", "information"),
    ("告诉我今天的新闻头条", "Mandarin", "information"),
    ("什么是人工智能?", "Mandarin", "information"),
    # Mandarin - Command
    ("设置早上七点的闹钟", "Mandarin", "command"),
    ("打开日历", "Mandarin", "command"),
    ("关灯", "Mandarin", "command"),
    ("打电话给妈妈", "Mandarin", "command"),

    # German - Entertainment
    ("Spiel mein Lieblingslied ab", "German", "entertainment"),
    ("Was ist gerade beliebt auf Netflix?", "German", "entertainment"),
    ("Empfiehl mir einen Podcast", "German", "entertainment"),
    ("Zeig mir Comedy-Sendungen", "German", "entertainment"),
    ("Spiel die neuesten Filmtrailer ab", "German", "entertainment"),
    # German - Navigation
    ("Bring mich zum Flughafen", "German", "navigation"),
    ("Wie komme ich zum Central Park?", "German", "navigation"),
    ("Finde das nächste Café", "German", "navigation"),
    ("Route nach Hause", "German", "navigation"),
    ("Wo ist die nächste Tankstelle?", "German", "navigation"),
    # German - Shopping
    ("Kauf neue Kopfhörer", "German", "shopping"),
    ("Bestell mir eine Pizza", "German", "shopping"),
    ("Verfolge meine Amazon-Bestellung", "German", "shopping"),
    ("Finde Bekleidungsgeschäfte in der Nähe", "German", "shopping"),
    ("Füge Milch zur Einkaufsliste hinzu", "German", "shopping"),
    # German - Information
    ("Wie ist das Wetter heute?", "German", "information"),
    ("Wer hat das Spiel gestern Abend gewonnen?", "German", "information"),
    ("Wie hoch ist der Eiffelturm?", "German", "information"),
    ("Sag mir die Schlagzeilen", "German", "information"),
    ("Definiere künstliche Intelligenz", "German", "information"),
    # German - Command
    ("Stell einen Wecker auf sieben Uhr", "German", "command"),
    ("Öffne den Kalender", "German", "command"),
    ("Mach das Licht aus", "German", "command"),
    ("Ruf Mama an", "German", "command"),

    # Japanese - Entertainment
    ("お気に入りの曲を再生して", "Japanese", "entertainment"),
    ("Netflixで何が人気?", "Japanese", "entertainment"),
    ("おすすめのポッドキャストを教えて", "Japanese", "entertainment"),
    ("最新の映画予告編を再生して", "Japanese", "entertainment"),
    ("コメディ番組を見せて", "Japanese", "entertainment"),
    # Japanese - Navigation
    ("空港まで連れて行って", "Japanese", "navigation"),
    ("セントラルパークへの行き方は?", "Japanese", "navigation"),
    ("一番近いカフェを探して", "Japanese", "navigation"),
    ("家までのルートを教えて", "Japanese", "navigation"),
    ("最寄りのガソリンスタンドはどこ?", "Japanese", "navigation"),
    # Japanese - Shopping
    ("新しいヘッドフォンを買って", "Japanese", "shopping"),
    ("ピザを注文して", "Japanese", "shopping"),
    ("Amazonの注文を追跡して", "Japanese", "shopping"),
    ("近くの洋服店を探して", "Japanese", "shopping"),
    ("買い物リストに牛乳を追加して", "Japanese", "shopping"),
    # Japanese - Information
    ("今日の天気はどう?", "Japanese", "information"),
    ("昨夜の試合は誰が勝った?", "Japanese", "information"),
    ("エッフェル塔の高さは?", "Japanese", "information"),
    ("今日のニュースの見出しを教えて", "Japanese", "information"),
    ("人工知能を定義して", "Japanese", "information"),
    # Japanese - Command
    ("朝7時にアラームをセットして", "Japanese", "command"),
    ("カレンダーを開いて", "Japanese", "command"),
    ("電気を消して", "Japanese", "command"),
    ("お母さんに電話して", "Japanese", "command"),

    # Portuguese - Entertainment
    ("Toque minha música favorita", "Portuguese", "entertainment"),
    ("O que está em alta na Netflix?", "Portuguese", "entertainment"),
    ("Recomende um podcast para mim", "Portuguese", "entertainment"),
    ("Mostre-me programas de comédia", "Portuguese", "entertainment"),
    # Portuguese - Navigation
    ("Me leve ao aeroporto", "Portuguese", "navigation"),
    ("Como chegar ao Central Park?", "Portuguese", "navigation"),
    ("Encontre o café mais próximo", "Portuguese", "navigation"),
    ("Rota para casa", "Portuguese", "navigation"),
    # Portuguese - Shopping
    ("Compre fones de ouvido novos", "Portuguese", "shopping"),
    ("Peça uma pizza para mim", "Portuguese", "shopping"),
    ("Rastreie meu pedido da Amazon", "Portuguese", "shopping"),
    ("Adicione leite à lista de compras", "Portuguese", "shopping"),
    # Portuguese - Information
    ("Como está o tempo hoje?", "Portuguese", "information"),
    ("Quem ganhou o jogo ontem à noite?", "Portuguese", "information"),
    ("Qual é a altura da Torre Eiffel?", "Portuguese", "information"),
    ("Me diga as manchetes de hoje", "Portuguese", "information"),
    # Portuguese - Command
    ("Coloque um alarme para as sete", "Portuguese", "command"),
    ("Abra o calendário", "Portuguese", "command"),
    ("Apague as luzes", "Portuguese", "command"),
    ("Ligue para a mamãe", "Portuguese", "command"),
]


def main():
    from collections import Counter

    random.seed(42)

    # Generate English queries by intent
    print("Generating English queries...")
    ent_queries = fill_entertainment()
    nav_queries = fill_navigation()
    shop_queries = fill_shopping()
    info_queries = fill_information()
    cmd_queries = fill_command()

    print(f"  Entertainment: {len(ent_queries)}")
    print(f"  Navigation:    {len(nav_queries)}")
    print(f"  Shopping:      {len(shop_queries)}")
    print(f"  Information:   {len(info_queries)}")
    print(f"  Command:       {len(cmd_queries)}")

    # Build English rows: (query_text, language, intent)
    english_rows = []
    for q in ent_queries:
        english_rows.append((q, "English", "entertainment"))
    for q in nav_queries:
        english_rows.append((q, "English", "navigation"))
    for q in shop_queries:
        english_rows.append((q, "English", "shopping"))
    for q in info_queries:
        english_rows.append((q, "English", "information"))
    for q in cmd_queries:
        english_rows.append((q, "English", "command"))

    total_english = len(english_rows)
    print(f"\nTotal unique English queries: {total_english}")

    # English should be ~90%, multilingual ~10%
    n_multi = len(MULTILINGUAL_QUERIES)
    target_english = int(n_multi * 9)  # 9:1 ratio
    print(f"Multilingual queries: {n_multi}")
    print(f"Target English for 90/10: {target_english}")

    if total_english > target_english:
        # Sample down English, keeping intent balance
        random.shuffle(english_rows)
        # Sample proportionally by intent
        per_intent = target_english // 5
        sampled = []
        for intent in ["entertainment", "navigation", "shopping", "information", "command"]:
            intent_rows = [r for r in english_rows if r[2] == intent]
            sampled.extend(intent_rows[:per_intent])
        # Fill remainder
        remaining_pool = [r for r in english_rows if r not in sampled]
        sampled.extend(remaining_pool[:target_english - len(sampled)])
        english_rows = sampled
    elif total_english < target_english:
        print(f"  NOTE: Only {total_english} unique English queries generated, using all.")

    # Combine
    all_rows = [(q, lang, intent) for q, lang, intent in english_rows]
    all_rows.extend(MULTILINGUAL_QUERIES)

    random.shuffle(all_rows)

    with open("voice_search_query_captures_multilingual.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["query_text", "language", "intent"])
        for q, lang, intent in all_rows:
            writer.writerow([q, lang, intent])

    total = len(all_rows)
    eng_count = sum(1 for _, lang, _ in all_rows if lang == "English")
    multi_count = total - eng_count

    print(f"\n{'='*50}")
    print(f"Final dataset: {total} rows (all unique)")
    print(f"English:       {eng_count} ({eng_count/total*100:.1f}%)")
    print(f"Multilingual:  {multi_count} ({multi_count/total*100:.1f}%)")

    # Per-language breakdown
    lang_dist = Counter(lang for _, lang, _ in all_rows)
    print(f"\nRows by language:")
    for lang, count in sorted(lang_dist.items(), key=lambda x: -x[1]):
        print(f"  {lang}: {count}")

    intent_dist = Counter(intent for _, _, intent in all_rows)
    print(f"\nRows by intent:")
    for intent, count in sorted(intent_dist.items(), key=lambda x: -x[1]):
        print(f"  {intent}: {count}")

    # Verify uniqueness
    all_texts = [q for q, _, _ in all_rows]
    assert len(all_texts) == len(set(all_texts)), "Duplicate queries found!"
    print(f"\nAll {total} queries are unique ✓")


if __name__ == "__main__":
    main()
