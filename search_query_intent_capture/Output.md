/Users/darshil.shah/Documents/my-projects/prototypes/venv/bin/python /Users/darshil.shah/Documents/my-projects/prototypes/search_query_intent_capture/main.py 
============================================================
TF-IDF CLUSTERING PIPELINE
============================================================

Loaded 1640 queries

── Building TF-IDF matrix ──
TF-IDF shape: (1640, 989)

── K-Means hyperparameter sweep ──
  K-Means k=3: silhouette=0.0206
  K-Means k=4: silhouette=0.0240
  K-Means k=5: silhouette=0.0304
  K-Means k=6: silhouette=0.0326
  K-Means k=7: silhouette=0.0387
  K-Means k=8: silhouette=0.0428
  K-Means k=9: silhouette=0.0549
  K-Means k=10: silhouette=0.0540

  Best k=9 (silhouette=0.0549)

── Top terms per cluster (K-Means k=9) ──
  Cluster 0: turn(0.393), lights(0.084), door(0.053), turn timer(0.035), turn lights(0.035), turn tv(0.034), turn oven(0.033), turn heater(0.033), turn thermostat(0.033), turn volume(0.033)
  Cluster 1: route(0.342), fastest route(0.116), fastest(0.116), scenic(0.104), scenic route(0.104), best route(0.085), best(0.066), route zoo(0.032), park(0.032), zoo(0.030)
  Cluster 2: order(0.383), online(0.195), replacement(0.171), order replacement(0.171), delivery(0.066), track(0.039), tent(0.022), skateboard(0.022), umbrella(0.022), sneakers(0.022)
  Cluster 3: drive(0.448), long drive(0.448), long(0.437), center(0.040), marina(0.030), mall(0.029), chicago(0.029), downtown(0.029), boston(0.029), stadium(0.029)
  Cluster 4: open(0.798), app(0.101), google(0.039), uber(0.038), youtube(0.037), email(0.037), spotify(0.037), camera(0.036), fitness(0.027), weather(0.026)
  Cluster 5: play(0.020), nearest(0.017), directions(0.013), navigate(0.013), add(0.012), deals(0.012), cheapest(0.011), near(0.011), set(0.011), capital(0.010)
  Cluster 6: does(0.374), work(0.192), cost(0.162), stand(0.106), time does(0.051), start(0.046), time(0.043), does electric(0.016), jacket cost(0.015), machine(0.014)
  Cluster 7: far(0.472), moscow(0.040), far moscow(0.040), far dentist(0.034), far gym(0.033), park(0.031), toronto(0.029), gym(0.029), sydney(0.028), berlin(0.028)
  Cluster 8: buy(0.367), nearby(0.148), buy new(0.126), new(0.112), buy gift(0.031), gift(0.031), best buy(0.029), headphones(0.028), drone(0.027), buy tickets(0.026)

── DBSCAN hyperparameter sweep ──
  DBSCAN eps=0.3: clusters=60, noise=1219, silhouette=0.7558
  DBSCAN eps=0.5: clusters=60, noise=492, silhouette=0.2015
  DBSCAN eps=0.7: clusters=7, noise=154, silhouette=0.0266
  DBSCAN eps=0.9: clusters=5, noise=103, silhouette=0.0255
  DBSCAN eps=1.0: clusters=1, noise=0, silhouette=-1.0000
  DBSCAN eps=1.2: clusters=1, noise=0, silhouette=-1.0000
  DBSCAN eps=1.5: clusters=1, noise=0, silhouette=-1.0000

  Best eps=0.3 (silhouette=0.7558, clusters=60)

── Top terms per cluster (DBSCAN eps=0.3) ──
  Cluster 0: case(0.506), phone case(0.506), phone(0.506), reviews(0.072), deals(0.067), online(0.066), cost(0.066), deal(0.062), best deal(0.062), buy(0.059)
  Cluster 1: water bottle(0.510), bottle(0.510), water(0.456), buy(0.128), reviews(0.087), cheapest(0.083), buy new(0.078), nearby(0.075), replacement(0.074), order replacement(0.074)
  Cluster 2: score(0.717), game(0.697), लग(0.000), german(0.000), ground(0.000), grocery store(0.000), grocery(0.000), great wall(0.000), great barrier(0.000), great(0.000)
  Cluster 3: spot(0.483), parking spot(0.483), parking(0.483), nearest parking(0.288), nearest(0.173), closest(0.085), far(0.075), navigate nearest(0.069), navigate(0.061), garage(0.000)
  Cluster 4: church(0.862), near(0.104), navigate(0.102), far(0.100), directions(0.100), great(0.000), goodbye(0.000), google(0.000), gravity(0.000), लग(0.000)
  Cluster 5: resistance(0.476), bands(0.476), resistance bands(0.476), buy resistance(0.147), buy(0.130), reviews(0.063), cheapest(0.060), online(0.058), buy new(0.056), deal(0.054)
  Cluster 6: running shoes(0.494), running(0.476), shoes(0.476), cheapest(0.071), deals(0.070), cost(0.068), buy new(0.067), best deal(0.063), deal(0.063), order replacement(0.063)
  Cluster 7: restock(1.000), लग(0.000), genre(0.000), ground(0.000), grocery store(0.000), grocery(0.000), great wall(0.000), great barrier(0.000), great(0.000), gravity(0.000)
  Cluster 8: play audiobook(0.605), audiobook(0.605), play(0.434), brown(0.122), great(0.000), giza(0.000), goodbye(0.000), google(0.000), gravity(0.000), लग(0.000)
  Cluster 9: time does(0.502), start(0.458), time(0.426), does(0.333), tournament(0.079), festival(0.079), premiere(0.077), concert(0.077), match(0.075), game(0.067)
  Cluster 10: stand(0.667), does(0.473), rsvp(0.064), unesco(0.064), mri(0.064), vpn(0.064), ai(0.064), ceo(0.063), nasa(0.060), germany(0.000)
  Cluster 11: meaning(1.000), लग(0.000), german(0.000), ground(0.000), grocery store(0.000), grocery(0.000), great wall(0.000), great barrier(0.000), great(0.000), gravity(0.000)
  Cluster 12: set timer(0.510), timer(0.480), set(0.420), minutes(0.276), 50(0.054), maximum(0.054), hour(0.051), 20(0.049), 30(0.047), 10 minutes(0.045)
  Cluster 13: hiking(0.486), boots(0.486), hiking boots(0.486), buy(0.082), reviews(0.057), cheapest(0.054), deals(0.053), cost(0.052), buy new(0.050), nearby(0.048)
  Cluster 14: central(0.485), central park(0.485), park(0.443), route central(0.128), route(0.073), directions central(0.068), zum(0.063), como(0.063), ao(0.063), wie(0.061)
  Cluster 15: long drive(0.487), drive(0.487), long(0.475), courthouse(0.093), waterfront(0.093), church(0.093), hospital(0.091), hotel(0.089), dentist(0.088), fusion(0.000)
  Cluster 16: francisco(0.483), san francisco(0.483), san(0.483), route san(0.151), route(0.089), directions(0.065), far(0.065), long drive(0.062), drive(0.062), best route(0.061)
  Cluster 17: set alarm(0.494), alarm(0.489), set(0.423), alarm pm(0.217), pm(0.207), alarm 10(0.083), 10(0.070), noon(0.051), 10 pm(0.036), downtown(0.000)
  Cluster 18: language(0.485), speak(0.485), language speak(0.485), morocco(0.040), chile(0.040), kenya(0.040), thailand(0.040), spain(0.040), germany(0.040), india(0.040)
  Cluster 19: conditioning(0.500), air conditioning(0.500), air(0.447), turn air(0.208), turn(0.133), resume(0.103), unlock(0.103), stop(0.091), hop(0.000), gas(0.000)
  Cluster 20: care(0.471), urgent(0.471), urgent care(0.471), nearest urgent(0.272), nearest(0.169), ahead(0.064), closest(0.064), near(0.060), directions nearest(0.053), navigate nearest(0.051)
  Cluster 21: house(0.513), mom house(0.513), mom(0.482), route mom(0.197), route(0.111), navigate(0.079), directions(0.077), best route(0.072), best(0.057), goodbye(0.000)
  Cluster 22: nominees(0.591), nominees year(0.591), year(0.549), grocery(0.000), great wall(0.000), great barrier(0.000), great(0.000), grocery store(0.000), genre(0.000), gravity(0.000)
  Cluster 23: open(1.000), लग(0.000), german(0.000), ground beef(0.000), ground(0.000), grocery store(0.000), grocery(0.000), great wall(0.000), great barrier(0.000), great(0.000)
  Cluster 24: stars(1.000), लग(0.000), genre(0.000), ground(0.000), grocery store(0.000), grocery(0.000), great wall(0.000), great barrier(0.000), great(0.000), gravity(0.000)
  Cluster 25: symptoms(0.967), food(0.079), लग(0.000), german(0.000), ground(0.000), grocery store(0.000), grocery(0.000), great wall(0.000), great barrier(0.000), great(0.000)
  Cluster 26: latest(0.492), play latest(0.492), album(0.483), play(0.341), eminem(0.107), coldplay(0.104), post(0.100), great(0.000), goodbye(0.000), google(0.000)
  Cluster 27: olympic(0.535), olympic games(0.535), games(0.478), distance(0.089), built(0.081), old(0.080), tell(0.078), origin(0.076), लग(0.000), gravity(0.000)
  Cluster 28: hits(0.671), play(0.437), 20(0.136), 100(0.136), 50(0.133), 10(0.122), game(0.000), games(0.000), ground beef(0.000), ground(0.000)
  Cluster 29: bag(0.499), sleeping bag(0.499), sleeping(0.485), order(0.110), reviews(0.077), cheapest(0.074), deals(0.072), online(0.070), cost(0.070), order replacement(0.064)
  Cluster 30: air purifier(0.501), purifier(0.501), air(0.449), order(0.126), 500(0.095), cheapest(0.083), rated(0.082), online(0.080), cost(0.080), replacement(0.074)
  Cluster 31: viral videos(0.519), videos(0.519), viral(0.519), tonight(0.104), tomorrow(0.095), right(0.094), today(0.094), german(0.000), germany(0.000), gift(0.000)
  Cluster 32: shopping list(0.423), list(0.423), shopping(0.423), add(0.368), salmon(0.041), tea(0.041), laundry(0.040), add bread(0.036), add butter(0.036), chicken(0.035)
  Cluster 33: rain(0.506), rain jacket(0.506), jacket(0.464), order(0.106), costco(0.088), reviews(0.076), cheapest(0.073), deals(0.071), nearby(0.065), replacement(0.064)
  Cluster 34: gaming(0.499), gaming mouse(0.499), mouse(0.499), buy(0.110), cheapest(0.069), deals(0.067), online(0.066), buy new(0.065), compare prices(0.062), prices(0.062)
  Cluster 35: capital(1.000), लग(0.000), german(0.000), ground beef(0.000), ground(0.000), grocery store(0.000), grocery(0.000), great wall(0.000), great barrier(0.000), great(0.000)
  Cluster 36: delivery(0.803), order(0.513), pizza(0.129), लग(0.000), germany(0.000), ground(0.000), grocery store(0.000), grocery(0.000), great wall(0.000), great barrier(0.000)
  Cluster 37: causes(1.000), लग(0.000), germany(0.000), ground beef(0.000), ground(0.000), grocery store(0.000), grocery(0.000), great wall(0.000), great barrier(0.000), great(0.000)
  Cluster 38: nasa(0.783), created(0.141), built(0.138), define(0.137), origin(0.132), gravity(0.000), gift(0.000), giza(0.000), goodbye(0.000), google(0.000)
  Cluster 39: switch(0.597), mode(0.597), focus(0.090), night(0.090), saving(0.090), dark(0.088), driving(0.085), gift(0.000), giza(0.000), goodbye(0.000)
  Cluster 40: fitness tracker(0.509), tracker(0.509), fitness(0.483), reviews(0.074), cheapest(0.071), deals(0.069), cost(0.068), nearby(0.064), deal(0.063), best deal(0.063)
  Cluster 41: mat(0.497), yoga mat(0.497), yoga(0.487), buy(0.106), order(0.105), reviews(0.072), deals(0.068), online(0.067), buy new(0.065), nearby(0.062)
  Cluster 42: theater(0.487), movie theater(0.487), movie(0.465), nearest movie(0.290), nearest(0.174), closest(0.086), near(0.080), directions nearest(0.072), directions(0.059), giza(0.000)
  Cluster 43: pyramids(0.515), pyramids giza(0.515), giza(0.515), wide(0.075), created(0.071), built(0.069), old(0.068), tell(0.067), origin(0.065), gift(0.000)
  Cluster 44: today deals(0.532), today(0.503), deals(0.407), target(0.095), doordash(0.095), foods(0.095), costco(0.095), best buy(0.085), best(0.054), buy(0.051)
  Cluster 45: playlist(0.703), play(0.505), focus(0.070), evening(0.069), road(0.069), workout(0.068), study(0.065), लग(0.000), google(0.000), giza(0.000)
  Cluster 46: work(0.752), does(0.337), driving(0.079), navigate(0.077), directions(0.076), far(0.076), great(0.000), gravity(0.000), google(0.000), german(0.000)
  Cluster 47: machu(0.508), machu picchu(0.508), picchu(0.508), old(0.092), origin(0.087), price(0.083), stock price(0.083), long(0.083), stock(0.081), google(0.000)
  Cluster 48: botanical(0.469), botanical garden(0.469), garden(0.469), route botanical(0.230), route(0.139), navigate(0.051), far(0.050), drive(0.047), long drive(0.047), best route(0.047)
  Cluster 49: united nations(0.504), united(0.504), nations(0.504), wide(0.102), tell(0.090), stock price(0.083), price(0.083), long(0.083), stock(0.081), friendly(0.000)
  Cluster 50: mahal(0.501), taj(0.501), taj mahal(0.501), wide(0.102), built(0.093), old(0.092), stock price(0.083), price(0.083), stock(0.081), great(0.000)
  Cluster 51: trench(0.526), mariana trench(0.526), mariana(0.526), created(0.097), built(0.093), tell(0.090), origin(0.087), google(0.000), goodbye(0.000), genre(0.000)
  Cluster 52: send text(0.499), text(0.492), send(0.448), boss(0.053), doctor(0.053), sarah(0.053), emily(0.053), mike(0.051), alex(0.051), dad(0.051)
  Cluster 53: tower(0.534), eiffel tower(0.534), eiffel(0.501), created(0.098), built(0.094), old(0.093), origin(0.089), gaming mouse(0.000), gift(0.000), ground beef(0.000)
  Cluster 54: city center(0.539), city(0.529), center(0.486), navigate(0.083), far(0.081), directions(0.081), long drive(0.077), drive(0.077), long(0.075), hop(0.000)
  Cluster 55: hardware(0.466), hardware store(0.466), store(0.410), nearest hardware(0.385), nearest(0.239), closest(0.091), directions nearest(0.075), navigate nearest(0.072), navigate(0.064), directions(0.062)
  Cluster 56: portable charger(0.526), portable(0.500), charger(0.486), buy(0.138), reviews(0.091), buy new(0.081), best deal(0.077), deal(0.077), new(0.072), best(0.066)
  Cluster 57: protein(0.486), protein powder(0.486), powder(0.486), best(0.135), cost(0.078), buy new(0.077), best deal(0.073), deal(0.073), replacement(0.072), order replacement(0.072)
  Cluster 58: ferry terminal(0.491), ferry(0.491), terminal(0.491), route ferry(0.154), route(0.087), far(0.064), long drive(0.062), drive(0.062), best route(0.060), long(0.060)
  Cluster 59: stream(0.581), live(0.581), festival(0.090), tournament(0.090), concert(0.088), premiere(0.088), match(0.086), game(0.078), gift(0.000), giza(0.000)

── K-Means stability (k=9, 10 runs) ──
  Mean pairwise ARI: 0.3923

── Cross-lingual note ──
  TF-IDF treats each language's tokens independently.
  Multilingual queries will NOT cluster with English equivalents.
  See embedding_clustering.py for cross-lingual clustering.

  TF-IDF pipeline completed in 0.9s
============================================================
MULTILINGUAL EMBEDDING CLUSTERING PIPELINE
============================================================

Loaded 1640 queries across 8 languages

── Encoding queries with sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 ──
Loading weights: 100%|██████████| 199/199 [00:00<00:00, 9278.30it/s]
BertModel LOAD REPORT from: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
Batches: 100%|██████████| 26/26 [00:00<00:00, 36.07it/s]
Embedding shape: (1640, 384)

── K-Means hyperparameter sweep ──
  K-Means k=3: silhouette=0.0804
  K-Means k=4: silhouette=0.0989
  K-Means k=5: silhouette=0.1132
  K-Means k=6: silhouette=0.1161
  K-Means k=7: silhouette=0.0942
  K-Means k=8: silhouette=0.0995
  K-Means k=9: silhouette=0.1045
  K-Means k=10: silhouette=0.1066

  Best k=6 (silhouette=0.1161)

── DBSCAN hyperparameter sweep ──
  DBSCAN eps=0.2: clusters=65, noise=1139, silhouette=0.6601
  DBSCAN eps=0.3: clusters=67, noise=653, silhouette=0.2680
  DBSCAN eps=0.4: clusters=16, noise=246, silhouette=-0.0872
  DBSCAN eps=0.5: clusters=4, noise=68, silhouette=0.0307
  DBSCAN eps=0.6: clusters=1, noise=8, silhouette=-1.0000
  DBSCAN eps=0.7: clusters=1, noise=0, silhouette=-1.0000
  DBSCAN eps=0.8: clusters=1, noise=0, silhouette=-1.0000
  DBSCAN eps=1.0: clusters=1, noise=0, silhouette=-1.0000

  Best eps=0.2 (silhouette=0.6601, clusters=65)

── Cross-lingual cluster analysis ──

  Language distribution per cluster (K-Means k=6):
  Cluster 0 (n=236, dominant_intent=information): English:223, Spanish:2, German:2, Japanese:2, French:2, Mandarin:2, Hindi:2, Portuguese:1
  Cluster 1 (n=371, dominant_intent=navigation): English:339, Japanese:5, German:5, Spanish:5, Mandarin:5, Hindi:4, French:4, Portuguese:4
  Cluster 2 (n=245, dominant_intent=entertainment): English:211, French:6, German:5, Japanese:5, Mandarin:5, Spanish:5, Portuguese:4, Hindi:4
  Cluster 3 (n=137, dominant_intent=command): English:126, Portuguese:2, Mandarin:2, French:2, Spanish:2, Hindi:1, Japanese:1, German:1
  Cluster 4 (n=272, dominant_intent=command): English:224, Hindi:9, French:7, German:7, Japanese:7, Portuguese:6, Spanish:6, Mandarin:6
  Cluster 5 (n=379, dominant_intent=shopping): English:353, Mandarin:4, Hindi:4, German:4, Spanish:4, Japanese:4, Portuguese:3, French:3

── Intent alignment ──

  Cluster → Intent mapping:
  Cluster 0: information (98.7% purity, n=236)
  Cluster 1: navigation (94.1% purity, n=371)
  Cluster 2: entertainment (88.2% purity, n=245)
  Cluster 3: command (100.0% purity, n=137)
  Cluster 4: command (43.0% purity, n=272)
  Cluster 5: shopping (92.1% purity, n=379)

── Frequent intent patterns ──

  Frequent query patterns per cluster:
  Cluster 0:
    "Who is the capital of France?" (x1)
    "Is the Constitution deep?" (x1)
    "What does AI stand for?" (x1)
    "What is the meaning of altruistic?" (x1)
    "What language do they speak in India?" (x1)
  Cluster 1:
    "Navigate to the stadium" (x1)
    "How far is Moscow from Berlin?" (x1)
    "सबसे नज़दीकी कॉफी शॉप ढूंढो" (x1)
    "Directions to the convention center" (x1)
    "Find the nearest grocery store" (x1)
  Cluster 2:
    "Recommend a book for a rainy day" (x1)
    "Recommend a science podcast" (x1)
    "Empfiehl mir einen Podcast" (x1)
    "Show me songs by Drake" (x1)
    "Stream tournament live" (x1)
  Cluster 3:
    "Start notifications" (x1)
    "Resume the heater" (x1)
    "Enable NFC" (x1)
    "Disable auto-rotate" (x1)
    "Stop emails" (x1)
  Cluster 4:
    "What time is it in Cairo?" (x1)
    "Show construction delays on my commute" (x1)
    "What's the weather in São Paulo?" (x1)
    "Take me to school" (x1)
    "Remind me to do laundry at 10 AM" (x1)
  Cluster 5:
    "Add eggs to my cart" (x1)
    "Show me reviews for coffee machine" (x1)
    "Buy phone case" (x1)
    "Show me home decor on sale" (x1)
    "Show me reviews for water bottle" (x1)

── K-Means stability (k=6, 10 runs) ──
  Mean pairwise ARI: 0.8365

  Embedding pipeline completed in 8.5s


============================================================
COMPARISON: TF-IDF vs MULTILINGUAL EMBEDDINGS
============================================================

── Best K-Means ──
  Metric                               TF-IDF   Embeddings
  ------------------------------------------------------
  Best k                                    9            6
  Silhouette                           0.0549       0.1161
  Purity                               0.3823       0.8543
  NMI                                  0.2326       0.6871
  ARI                                  0.0064       0.6746
  Stability (ARI, 10 runs)             0.3923       0.8365

── At k=5 (true intent count) ──
  Metric                               TF-IDF   Embeddings
  ------------------------------------------------------
  Silhouette                           0.0304       0.1132
  Purity                               0.3299       0.9061
  NMI                                  0.1599       0.7458
  ARI                                  0.0138       0.7840

── Cross-lingual clustering quality (best K-Means) ──
  Metric                               TF-IDF   Embeddings
  ------------------------------------------------------
  Mean normalized lang entropy         0.0460       0.2464
  (1.0 = perfect language mixing across clusters)

── Generating plots ──
  Saved: plot_tfidf_kmeans.png
  Saved: plot_embedding_kmeans.png
  Saved: plot_embedding_dbscan.png
  Saved: silhouette_comparison.png


============================================================
QUERY SUGGESTION DEMONSTRATION
============================================================
Loading weights: 100%|██████████| 199/199 [00:00<00:00, 25214.99it/s]
BertModel LOAD REPORT from: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

  Query: "Play some music"
  Cluster-based suggestions:
    [2] Play {genre} music (sim=0.882)
    [2] Play intense music for reading (sim=0.752)
    [2] Spiel mein Lieblingslied ab (sim=0.750)
    [2] Play upbeat music for dinner (sim=0.747)
    [2] Play happy music for studying (sim=0.740)
  Naive nearest-neighbour:
    [2] Play {genre} music (sim=0.882)
    [2] Play intense music for reading (sim=0.752)
    [2] Spiel mein Lieblingslied ab (sim=0.750)
    [2] Play upbeat music for dinner (sim=0.747)
    [2] Play happy music for studying (sim=0.740)

  Query: "How do I get to the mall?"
  Cluster-based suggestions:
    [1] How do I get to the mall? (sim=1.000)
    [1] ¿Cómo llego al centro comercial? (sim=0.980)
    [1] What's the best route to the mall? (sim=0.829)
    [1] Take me to the mall (sim=0.791)
    [1] How long to drive to the mall? (sim=0.741)
  Naive nearest-neighbour:
    [1] How do I get to the mall? (sim=1.000)
    [1] ¿Cómo llego al centro comercial? (sim=0.980)
    [1] What's the best route to the mall? (sim=0.829)
    [1] Take me to the mall (sim=0.791)
    [1] How long to drive to the mall? (sim=0.741)

  Query: "Order food online"
  Cluster-based suggestions:
    [5] Track my Whole Foods order (sim=0.733)
    [5] Order umbrella online (sim=0.586)
    [5] Order keyboard online (sim=0.576)
    [5] Order tent online (sim=0.566)
    [5] Order tablet online (sim=0.564)
  Naive nearest-neighbour:
    [5] Track my Whole Foods order (sim=0.733)
    [4] Show me today's deals on Whole Foods (sim=0.590)
    [5] Order umbrella online (sim=0.586)
    [5] Order keyboard online (sim=0.576)
    [5] Order tent online (sim=0.566)

  Query: "What's the temperature outside?"
  Cluster-based suggestions:
    [4] ¿Cuál es el clima de hoy? (sim=0.722)
    [4] Quel temps fait-il aujourd'hui? (sim=0.690)
    [4] Wie ist das Wetter heute? (sim=0.682)
    [4] 今日の天気はどう? (sim=0.670)
    [4] Como está o tempo hoje? (sim=0.666)
  Naive nearest-neighbour:
    [4] ¿Cuál es el clima de hoy? (sim=0.722)
    [4] Quel temps fait-il aujourd'hui? (sim=0.690)
    [4] Wie ist das Wetter heute? (sim=0.682)
    [4] 今日の天気はどう? (sim=0.670)
    [4] Como está o tempo hoje? (sim=0.666)

  Query: "Set a timer"
  Cluster-based suggestions:
    [3] Set a timer for 1 hour (sim=0.899)
    [3] Turn up the timer (sim=0.872)
    [3] Set a timer for 10 minutes (sim=0.850)
    [3] Set a timer for 15 minutes (sim=0.847)
    [3] Set a timer for 30 minutes (sim=0.846)
  Naive nearest-neighbour:
    [3] Set a timer for 1 hour (sim=0.899)
    [3] Turn up the timer (sim=0.872)
    [3] Set a timer for 10 minutes (sim=0.850)
    [3] Set a timer for 15 minutes (sim=0.847)
    [3] Set a timer for 30 minutes (sim=0.846)

  Query: "Compra algo en línea"
  Cluster-based suggestions:
    [5] Order umbrella online (sim=0.554)
    [5] Order camera online (sim=0.540)
    [5] Order sneakers online (sim=0.537)
    [5] Order tent online (sim=0.535)
    [5] Verfolge meine Amazon-Bestellung (sim=0.523)
  Naive nearest-neighbour:
    [5] Order umbrella online (sim=0.554)
    [5] Order camera online (sim=0.540)
    [5] Order sneakers online (sim=0.537)
    [5] Order tent online (sim=0.535)
    [5] Verfolge meine Amazon-Bestellung (sim=0.523)

  Query: "最近のニュースを教えて"
  Cluster-based suggestions:
    [4] 今日のニュースの見出しを教えて (sim=0.841)
    [4] Me diga as manchetes de hoje (sim=0.820)
    [4] Sag mir die Schlagzeilen (sim=0.806)
    [4] 告诉我今天的新闻头条 (sim=0.804)
    [4] Donne-moi les titres des actualités (sim=0.788)
  Naive nearest-neighbour:
    [4] 今日のニュースの見出しを教えて (sim=0.841)
    [4] Me diga as manchetes de hoje (sim=0.820)
    [4] Sag mir die Schlagzeilen (sim=0.806)
    [4] 告诉我今天的新闻头条 (sim=0.804)
    [4] Donne-moi les titres des actualités (sim=0.788)

  Query: "Wie wird das Wetter morgen?"
  Cluster-based suggestions:
    [4] 今日の天気はどう? (sim=0.857)
    [4] 今天天气怎么样? (sim=0.842)
    [4] Quel temps fait-il aujourd'hui? (sim=0.842)
    [4] Wie ist das Wetter heute? (sim=0.839)
    [4] Como está o tempo hoje? (sim=0.834)
  Naive nearest-neighbour:
    [4] 今日の天気はどう? (sim=0.857)
    [4] 今天天气怎么样? (sim=0.842)
    [4] Quel temps fait-il aujourd'hui? (sim=0.842)
    [4] Wie ist das Wetter heute? (sim=0.839)
    [4] Como está o tempo hoje? (sim=0.834)

============================================================
RETRIEVAL GROUPING DEMONSTRATION
============================================================

  6 clusters discovered:

  Cluster 0 — "information" (purity=98.7%, size=236)
    Sample queries:
      - Who invented Machu Picchu?
      - How old is Mount Everest?
      - How does the greenhouse effect work?
      - What is relativity?
      - What is dark matter?
      - How does blockchain work?

  Cluster 1 — "navigation" (purity=94.1%, size=371)
    Sample queries:
      - How far is the gym from here?
      - Find the nearest ATM
      - Route avoiding traffic
      - Take me to the nearest auto repair shop
      - How far is it to the next pharmacy?
      - Show me the fastest route to Miami

  Cluster 2 — "entertainment" (purity=88.2%, size=245)
    Sample queries:
      - Who stars in Barbie?
      - Stream premiere live
      - 播放我喜欢的歌
      - Show me {genre} movies
      - What's new on Peacock?
      - Play intense music for driving

  Cluster 3 — "command" (purity=100.0%, size=137)
    Sample queries:
      - Turn up the volume
      - Stop emails
      - Turn up the brightness
      - Cancel my emails
      - Stop voicemail
      - Turn off the garage door

  Cluster 4 — "command" (purity=43.0%, size=272)
    Sample queries:
      - Send a text to Mike
      - Pide una pizza para mí
      - Stell einen Wecker auf sieben Uhr
      - Take me to the university
      - Reply to the restaurant's message
      - What games are on Sunday?

  Cluster 5 — "shopping" (purity=92.1%, size=379)
    Sample queries:
      - Open the banking app
      - Buy portable charger
      - Find deals on laptop
      - Find a EV charger near me
      - Find the best deal on office chair
      - Order a replacement tent

  KEY INSIGHT: Clustering groups semantically similar queries across
  languages, surface forms, and phrasings into coherent intent buckets.
  This enables:
    1. Intent-aware suggestions (suggest within same intent cluster)
    2. Multilingual query expansion (find equivalent queries in other languages)
    3. Retrieval re-ranking (boost results matching the query's cluster intent)

============================================================
PIPELINE COMPLETE
============================================================