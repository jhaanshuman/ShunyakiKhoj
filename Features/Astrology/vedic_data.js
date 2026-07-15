// Vedic Astrological Glossary and Festival Rules Data
window.VEDIC_DATA = {
    // ── GLOSSARY DATA ────────────────────────────────────────────────────────
    glossary: {
        // Core Limbs
        "tithi": "Tithi represents the lunar day, calculated based on the angular distance between the Sun and the Moon (12 degrees per Tithi). There are 30 Tithis in a lunar month.",
        "nakshatra": "Nakshatras are the 27 stellar constellations/divisions of the ecliptic plane, each spanning 13 degrees and 20 minutes, indicating where the Moon resides.",
        "yoga": "Yoga is calculated by summing the longitudes of the Sun and the Moon, divided into 27 equal parts of 13°20' each. It represents dynamic cosmic energy.",
        "karana": "Karana is half of a Tithi (6 degrees of longitudinal elongation difference). There are 11 Karanas: 7 recurring (movable) and 4 fixed.",
        "var": "Var represents the solar day of the week, running from sunrise to the next sunrise, named after planetary deities.",
        "panchang": "Panchang refers to the 'Five Limbs' of Vedic timekeeping: Tithi, Nakshatra, Yoga, Karana, and Var, used to calculate auspicious timings.",
        "lunar month": "A lunar month is the period from one new moon to the next (Amanta) or one full moon to the next (Purnimanta), containing 30 tithis.",

        // Months
        "chaitra": "Chaitra is the 1st month of the Hindu calendar (March-April), marks the beginning of the New Year (Varsha Pratipada).",
        "vaishakha": "Vaishakha is the 2nd month (April-May), associated with high heat and the auspicious Akshaya Tritiya.",
        "jyeshtha": "Jyeshtha is the 3rd month (May-June), associated with the summer solstice and Ganga Dussehra.",
        "ashadha": "Ashadha is the 4th month (June-July), marks the onset of monsoon and Guru Purnima.",
        "shravana": "Shravana is the 5th month (July-August), highly sacred to Lord Shiva, featuring Raksha Bandhan.",
        "bhadrapada": "Bhadrapada is the 6th month (August-September), features Ganesha Chaturthi and Janmashtami.",
        "ashwina": "Ashwina is the 7th month (September-October), hosts Shardiya Navratri, Dussehra, and Durga Puja.",
        "kartika": "Kartika is the 8th month (October-November), considered the holiest month, featuring Diwali and Kartik Snan.",
        "margashirsha": "Margashirsha is the 9th month (November-December), highly revered in Bhagavad Gita where Krishna calls it Himself.",
        "pausha": "Pausha is the 10th month (December-January), features solar transit into Capricorn (Makar Sankranti).",
        "magha": "Magha is the 11th month (January-February), associated with sacred river bathing and Vasant Panchami.",
        "phalguna": "Phalguna is the 12th and final month (February-March), featuring Maha Shivaratri and Holi.",

        // Nakshatras
        "ashwini": "Ashwini is the 1st Nakshatra, ruled by Ketu, symbolized by a horse's head, representing speed, healing, and energy.",
        "bharani": "Bharani is the 2nd Nakshatra, ruled by Venus and Yama, representing bearing, transformation, and fire.",
        "krittika": "Krittika is the 3rd Nakshatra, ruled by Sun and Agni, representing cutting, purification, and sharpness.",
        "rohini": "Rohini is the 4th Nakshatra, ruled by Moon and Brahma, representing growth, fertility, beauty, and art.",
        "mrigashira": "Mrigashira is the 5th Nakshatra, ruled by Mars, symbolized by a deer, representing search, travel, and curiosity.",
        "ardra": "Ardra is the 6th Nakshatra, ruled by Rahu and Rudra, representing moistness, storms, tears, and intellectual clarity.",
        "punarvasu": "Punarvasu is the 7th Nakshatra, ruled by Jupiter and Aditi, representing return of light, safety, and renewal.",
        "pushya": "Pushya is the 8th Nakshatra, ruled by Saturn and Brihaspati, considered the most nurturing and auspicious for spiritual work.",
        "ashlesha": "Ashlesha is the 9th Nakshatra, ruled by Mercury and Serpent deities, representing mystique, poison, and hypnotic power.",
        "magha": "Magha is the 10th Nakshatra, ruled by Ketu and Pitris (ancestors), representing royalty, power, and heritage.",
        "purva phalguni": "Purva Phalguni is the 11th Nakshatra, ruled by Venus, representing relaxation, romance, creativity, and luck.",
        "uttara phalguni": "Uttara Phalguni is the 12th Nakshatra, ruled by Sun, representing relationships, charity, and social duty.",
        "hasta": "Hasta is the 13th Nakshatra, ruled by Moon, symbolized by a hand, representing craftsmanship, skill, and intellect.",
        "chitra": "Chitra is the 14th Nakshatra, ruled by Mars and Vishwakarma, representing architecture, design, gems, and brilliance.",
        "swati": "Swati is the 15th Nakshatra, ruled by Rahu, representing independence, wind, movement, and flexibility.",
        "vishakha": "Vishakha is the 16th Nakshatra, ruled by Jupiter and Indra-Agni, representing focused goals and triumph.",
        "anuradha": "Anuradha is the 17th Nakshatra, ruled by Saturn and Mitra, representing friendship, cooperation, and devotion.",
        "jyeshtha": "Jyeshtha is the 18th Nakshatra, ruled by Mercury and Indra, representing seniority, protection, and esoteric power.",
        "mula": "Mula is the 19th Nakshatra, ruled by Ketu and Nirriti, representing roots, investigation, and destruction of ego.",
        "purva ashadha": "Purva Ashadha is the 20th Nakshatra, ruled by Venus, representing invincibility, declaration of war, and water.",
        "uttara ashadha": "Uttara Ashadha is the 21st Nakshatra, ruled by Sun, representing universal victory and enduring success.",
        "shravana": "Shravana is the 22nd Nakshatra, ruled by Moon and Vishnu, representing listening, oral traditions, and learning.",
        "dhanishtha": "Dhanishtha is the 23rd Nakshatra, ruled by Mars and Vasus, representing wealth, music, and social fame.",
        "shatabhisha": "Shatabhisha is the 24th Nakshatra, ruled by Rahu, representing 100 healers, secrecy, and high cosmic vision.",
        "purva bhadrapada": "Purva Bhadrapada is the 25th Nakshatra, ruled by Jupiter, representing spiritual heat, passion, and transformation.",
        "uttara bhadrapada": "Uttara Bhadrapada is the 26th Nakshatra, ruled by Saturn, representing deep wisdom, rest, and Kundalini energy.",
        "revati": "Revati is the 27th Nakshatra, ruled by Mercury and Pushan, representing journey, completion, protection, and transition.",

        // Yogas
        "vishkambha": "Vishkambha Yoga (1st): represents obstacles or support pillars; overall neutral to challenging.",
        "priti": "Priti Yoga (2nd): represents love, fondness, and joy; highly auspicious for social activities.",
        "ayushmana": "Ayushmana Yoga (3rd): represents longevity and health; good for starting wellness regimens.",
        "saubhagya": "Saubhagya Yoga (4th): represents good fortune and prosperity; auspicious for marriages.",
        "shobhana": "Shobhana Yoga (5th): represents beauty and excellence; good for aesthetic work.",
        "atiganda": "Atiganda Yoga (6th): represents severe obstacles or danger; inauspicious for major events.",
        "sukarma": "Sukarma Yoga (7th): represents noble deeds and successful efforts; good for starting jobs.",
        "dhriti": "Dhriti Yoga (8th): represents patience and joy; auspicious for foundation laying.",
        "shula": "Shula Yoga (9th): represents pain or conflict; inauspicious, best avoided for new travels.",
        "ganda": "Ganda Yoga (10th): represents defects or challenges; inauspicious for key beginnings.",
        "vriddhi": "Vriddhi Yoga (11th): represents growth and expansion; highly auspicious for investments.",
        "dhruva": "Dhruva Yoga (12th): represents constancy and determination; good for permanent works.",
        "vyaghata": "Vyaghata Yoga (13th): represents sudden shocks or combativeness; inauspicious.",
        "harshana": "Harshana Yoga (14th): represents happiness and thrills; auspicious for celebrations.",
        "vajra": "Vajra Yoga (15th): represents diamond-like strength or thunderbolts; neutral.",
        "siddhi": "Siddhi Yoga (16th): represents accomplishment and realization; excellent for starting ventures.",
        "vyatipata": "Vyatipata Yoga (17th): represents sudden calamity or reverse energy; inauspicious.",
        "variyana": "Variyana Yoga (18th): represents luxury and comfort; good for buying properties.",
        "parigha": "Parigha Yoga (19th): represents lock-up gates or fences; bad for beginning travels.",
        "shiva": "Shiva Yoga (20th): represents auspiciousness and purity; highly sacred and beneficial.",
        "siddha": "Siddha Yoga (21st): represents perfection and absolute capability; highly auspicious.",
        "sadhya": "Sadhya Yoga (22nd): represents feasibility and dedication; good for learning.",
        "shubha": "Shubha Yoga (23rd): represents overall auspiciousness and clean luck; highly positive.",
        "shukla": "Shukla Yoga (24th): represents bright and pure energy; highly auspicious.",
        "brahma": "Brahma Yoga (25th): represents creation and wisdom; excellent for studies.",
        "indra": "Indra Yoga (26th): represents leadership and governance; good for authority work.",
        "vaidhriti": "Vaidhriti Yoga (27th): represents total chaotic energy; inauspicious.",

        // Karanas
        "kinstughna": "Kinstughna Karana: The first fixed Karana, auspicious for charity and general ceremonies.",
        "bava": "Bava Karana: Active during growing phases; auspicious for health, growth, and starting actions.",
        "balava": "Balava Karana: Auspicious for spiritual ceremonies, study, and stable activities.",
        "kaulava": "Kaulava Karana: Auspicious for friendships, treaties, and domestic relationships.",
        "taitila": "Taitila Karana: Auspicious for housing, craft, courage, and general activities.",
        "garaja": "Garaja Karana: Auspicious for agricultural works, buying seeds, and solid labor.",
        "vanija": "Vanija Karana: Highly auspicious for trading, transactions, and beginning businesses.",
        "vishti": "Vishti Karana (Bhadra): Considered highly inauspicious; major works are avoided during Vishti.",
        "shakuni": "Shakuni Karana: Fixed Karana; auspicious for medicines, therapy, and healing.",
        "chatushpada": "Chatushpada Karana: Fixed Karana; auspicious for cattle, state affairs, and ancestry rites.",
        "nagava": "Nagava Karana: Fixed Karana; associated with serpentine energies, good for deep search.",

        // Tithis
        "pratipada": "Pratipada (1st lunar day): Good for ceremonies, sowing, and journeys.",
        "dwitiya": "Dwitiya (2nd lunar day): Auspicious for marriage, foundation laying, and music.",
        "tritiya": "Tritiya (3rd lunar day): Auspicious for weddings, tonsure (Mundan), and buying ornaments.",
        "chaturthi": "Chaturthi (4th lunar day): Ruled by Ganesha; good for obstacle removal, bad for journeys.",
        "panchami": "Panchami (5th lunar day): Highly auspicious for education, farming, and medicine.",
        "shashthi": "Shashthi (6th lunar day): Ruled by Kartikeya; good for battles, building, and state affairs.",
        "saptami": "Saptami (7th lunar day): Ruled by Sun; auspicious for buying vehicles and starting journeys.",
        "ashtami": "Ashtami (8th lunar day): Ruled by Durga; auspicious for battles, dynamic events, and fasts.",
        "navami": "Navami (9th lunar day): Ruled by Rama; good for dynamic combat, bad for auspicious beginnings.",
        "dashami": "Dashami (10th lunar day): Highly auspicious for government work, trade, and ceremonies.",
        "ekadashi": "Ekadashi (11th lunar day): Highly sacred for fasting and worship of Lord Vishnu.",
        "dwadashi": "Dwadashi (12th lunar day): Good for religious deeds, reading texts, and lighting lamps.",
        "trayodashi": "Trayodashi (13th lunar day): Pradosha time; sacred for Lord Shiva worship and fasts.",
        "chaturdashi": "Chaturdashi (14th lunar day): Auspicious for Shivaratri worship, bad for general travel.",
        "purnima": "Purnima (15th/Full Moon day): Marks peak lunar energy; auspicious for pujas and feasts.",
        "amavasya": "Amavasya (30th/New Moon day): Day of ancestors; auspicious for Pitru rites and donation.",

        // Rashis
        "mesha": "Mesha (Aries): Ruled by Mars; representing initiation, fire, energy, and leadership.",
        "vrishabha": "Vrishabha (Taurus): Ruled by Venus; representing stability, finance, art, and endurance.",
        "mithuna": "Mithuna (Gemini): Ruled by Mercury; representing communication, duality, logic, and arts.",
        "karka": "Karka (Cancer): Ruled by Moon; representing emotion, home, water, and care.",
        "simha": "Simha (Leo): Ruled by Sun; representing royalty, courage, creativity, and authority.",
        "kanya": "Kanya (Virgo): Ruled by Mercury; representing intellect, calculation, details, and health.",
        "tula": "Tula (Libra): Ruled by Venus; representing balance, partnerships, design, and commerce.",
        "vrishchika": "Vrishchika (Scorpio): Ruled by Mars; representing mysteries, depth, transformation, and water.",
        "dhanu": "Dhanu (Sagittarius): Ruled by Jupiter; representing philosophy, higher goals, fire, and archery.",
        "makara": "Makara (Capricorn): Ruled by Saturn; representing career, discipline, structure, and earth.",
        "kumbha": "Kumbha (Aquarius): Ruled by Saturn; representing networks, humanity, innovation, and air.",
        "meena": "Meena (Pisces): Ruled by Jupiter; representing imagination, spirituality, moksha, and water.",

        // Anandadi Yogas
        "ananda": "Ananda Yoga: Highly auspicious, brings joy, happiness, and absolute success.",
        "kaladanda": "Kaladanda Yoga: Auspicious to neutral, represents cosmic boundaries.",
        "mrityu": "Mrityu Yoga: Highly inauspicious, signals danger, failure, or major delays.",
        "dhumra": "Dhumra Yoga: Inauspicious, clouds judgment and creates confusion.",
        "asukha": "Asukha Yoga: Inauspicious, causes distress or physical discomfort.",
        "dhata": "Dhata / Prajapati Yoga: Auspicious, good for creation, building, and initiating.",
        "prajapati": "Prajapati Yoga: Auspicious, good for long-term construction and farming.",
        "saumya": "Saumya Yoga: Auspicious, brings calm, peace, and friendly relations.",
        "bahu sukha": "Bahu Sukha Yoga: Highly auspicious, promises multi-fold joy and happiness.",
        "dhwanksha": "Dhwanksha Yoga: Inauspicious, causes loss of assets and failure.",
        "dhanakshaya": "Dhanakshaya Yoga: Inauspicious, indicates financial losses or bad investments.",
        "ketu": "Ketu Yoga: Inauspicious to neutral, good for spiritual focus but bad for worldly works.",
        "dhwaja": "Dhwaja Yoga: Auspicious, brings victory, promotion, and status elevation.",
        "shrivatsa": "Shrivatsa Yoga: Highly auspicious, brings wealth, grace, and family happiness.",
        "saukhyasampatti": "Saukhyasampatti Yoga: Highly auspicious, promises comfort and asset growth.",
        "kshaya": "Kshaya Yoga: Inauspicious, drains energy and leads to waste.",
        "mudgara": "Mudgara Yoga: Inauspicious, leads to conflicts and physical blocks.",
        "lakshmikshaya": "Lakshmikshaya Yoga: Inauspicious, indicates loss of prosperity and wealth.",
        "chhatra": "Chhatra Yoga: Auspicious, provides shelter, protection, and safety.",
        "rajasanmana": "Rajasanmana Yoga: Highly auspicious, brings honor from elders or authorities.",
        "mitra": "Mitra Yoga: Auspicious, brings help from friends and successful teamwork.",
        "pushti": "Pushti Yoga: Auspicious, represents nourishment, recovery, and strength.",
        "manasa": "Manasa Yoga: Auspicious, brings mental peace and intellectual clarity.",
        "padma": "Padma Yoga: Highly auspicious, brings wealth, spiritual purity, and fortune.",
        "dhanagama": "Dhanagama Yoga: Auspicious, indicates arrival of cash flow or assets.",
        "lumbaka": "Lumbaka Yoga: Inauspicious, indicates sudden blocks or drop in power.",
        "utpata": "Utpata Yoga: Highly inauspicious, brings sudden accidents, shocks, or fire.",
        "prananasha": "Prananasha Yoga: Highly inauspicious, indicates critical danger or health threat.",
        "kana": "Kana Yoga: Inauspicious, indicates sensory blocks or lack of clarity.",
        "klesha": "Klesha Yoga: Inauspicious, causes mental worry, pain, and arguments.",
        "karyasiddhi": "Karyasiddhi Yoga: Highly auspicious, guarantees success in targeted tasks.",
        "kalyana": "Kalyana Yoga: Highly auspicious, brings holy events, weddings, and welfare.",
        "amrita": "Amrita Yoga: Most auspicious, bestows immortality of action, nectar-like success.",
        "mushala": "Mushala Yoga: Inauspicious, hard labor with zero rewards.",
        "gada": "Gada Yoga: Inauspicious, indicates injury, physical pain, or combat.",
        "bhaya": "Bhaya Yoga: Inauspicious, brings fear, anxiety, and insecurity.",
        "matanga": "Matanga Yoga: Auspicious, represents elephant-like strength and royalty.",
        "kulavriddhi": "Kulavriddhi Yoga: Highly auspicious, promises lineage growth and family prosperity.",
        "rakshasa": "Rakshasa Yoga: Highly inauspicious, demonic energy causing extreme chaos.",
        "mahakashta": "Mahakashta Yoga: Inauspicious, extreme hardship and pain.",
        "chara": "Chara Yoga: Auspicious, good for mobile works, driving, and starting journeys.",
        "sthira": "Sthira Yoga: Auspicious, excellent for foundation stone laying and building.",
        "griharambha": "Griharambha Yoga: Auspicious, specifically for beginning home construction.",
        "vardhamana": "Vardhamana Yoga: Highly auspicious, increases assets continuously.",
        "vivaha": "Vivaha Yoga: Highly auspicious, specifically for marriage ceremonies.",

        // Samvatsaras
        "prabhava": "Prabhava (1st): Beginning of the 60-year cycle; brings progress and new creations.",
        "vibhava": "Vibhava (2nd): Brings luxury, comfort, and general material prosperity.",
        "shukla": "Shukla (3rd): Pure, brings excellent crops and peace to society.",
        "pramoda": "Pramoda (4th): Joyous year; brings art, music, and high welfare.",
        "prajapati": "Prajapati (5th): Auspicious for construction and agricultural expansion.",
        "angira": "Angira (6th): Wise year; promotes research, education, and philosophies.",
        "shrimukha": "Shrimukha (7th): Brings fame, beautiful events, and general fortune.",
        "bhava": "Bhava (8th): Promotes emotional growth, arts, and stable relationships.",
        "yuva": "Yuva (9th): Energetic year; youthful vigor, expansion, and travel.",
        "dhata": "Dhata (10th): Auspicious for investments, business setup, and savings.",
        "ishwara": "Ishwara (11th): Divine protection; good for temples, charities, and justice.",
        "bahudhanya": "Bahudhanya (12th): Year of multi-fold grains; abundant crops and food.",
        "pramathi": "Pramathi (13th): Intense year; conflicts or heavy weather changes possible.",
        "vikrama": "Vikrama (14th): Valiant year; brings political changes and bold actions.",
        "vrisha": "Vrisha (15th): Stable, cattle growth, and general financial strength.",
        "chitrabhanu": "Chitrabhanu (16th): Bright, solar energy, inventions, and light.",
        "subhanu": "Subhanu (17th): Auspicious, general peace and health improvements.",
        "tarana": "Tarana (18th): Crossing hurdles; success after fighting obstacles.",
        "parthiva": "Parthiva (19th): Earthy year; good for land purchase and construction.",
        "vyaya": "Vyaya (20th): High expenses; focus on spiritual charity rather than savings.",
        "sarvajit": "Sarvajit (21st): Conquering all; brings success in legal affairs and battles.",
        "sarvadhari": "Sarvadhari (22nd): Sustaining all; solid social security and relief.",
        "virodhi": "Virodhi (23rd): Opposition; rise of debates, disputes, and protests.",
        "vikriti": "Vikriti (24th): Year of unusual occurrences, weather anomalies, or shifts.",
        "khara": "Khara (25th): Harsh conditions; requires caution in banking and food stocks.",
        "nandana": "Nandana (26th): Joyful, birth of children, general family celebrations.",
        "vijaya": "Vijaya (27th): Year of absolute victory in all efforts and projects.",
        "jaya": "Jaya (28th): Highly auspicious for victory in competitive exams.",
        "manmatha": "Manmatha (29th): Focus on love, beauty, fashion, and social life.",
        "durmukha": "Durmukha (30th): Harsh speech or diplomatic disputes in society.",
        "hemalambi": "Hemalambi (31st): Golden year; gold price rise, massive asset growth.",
        "vilambi": "Vilambi (32nd): Delay year; things move slowly but steadily.",
        "vikari": "Vikari (33rd): Disease or sudden shifts; focus on healthcare and hygiene.",
        "sharvari": "Sharvari (34th): Night-like; secretive operations, deep spiritual works.",
        "plava": "Plava (35th): Floods or high rains; travel via ships and water projects.",
        "shubhakrit": "Shubhakrit (36th): Creation of holy events; marriages and peace.",
        "shobhakrit": "Shobhakrit (37th): Brilliant deeds; artistic achievements and glory.",
        "krodhi": "Krodhi (38th): Anger or sudden strikes; requires diplomatic patience.",
        "vishvavasu": "Vishvavasu (39th): Auspicious for international trades and music.",
        "parabhava": "Parabhava (40th): Defeat of bad actors; legal victories for the truth.",
        "plavanga": "Plavanga (41st): Jump like monkeys; sudden market swings and travel.",
        "kilaka": "Kilaka (42nd): Standardized, structural developments and treaties.",
        "saumya": "Saumya (43rd): Highly peaceful; rise in education and intellectual pursuits.",
        "sadharana": "Sadharana (44th): Average or steady year; good for normal routines.",
        "virodhakrit": "Virodhakrit (45th): Rise in oppositions and labor union protests.",
        "paridhavi": "Paridhavi (46th): Protection; good for boundary walls and defense forces.",
        "pramadi": "Pramadi (47th): Sloth or errors; double-check calculations and contracts.",
        "aananda": "Aananda (48th): Extremely joyful year; high prosperity and general welfare.",
        "rakshasa": "Rakshasa (49th): Demonic energies active; rise of dynamic defense actions.",
        "nala": "Nala (50th): Auspicious, rise of water projects, canals, and shipping.",
        "pingala": "Pingala (51st): Warm energy; solar power, fire projects, and metallurgy.",
        "kalayukta": "Kalayukta (52nd): Time-bound changes; deep historical developments.",
        "siddharthi": "Siddharthi (53rd): Fulfillment of wishes; highly auspicious for starting projects.",
        "raudra": "Raudra (54th): Intense energy, storm years, worship of Rudra.",
        "durmati": "Durmati (55th): Poor judgment in leadership; requires public patience.",
        "dundubhi": "Dundubhi (56th): Victory drums; fame, public announcements, and success.",
        "rudhirodgari": "Rudhirodgari (57th): Red energy; focus on blood donations and defense health.",
        "raktaksha": "Raktaksha (58th): Alert eyes; rise of cybersecurity and defense watch.",
        "krodhana": "Krodhana (59th): Intense arguments; good for court litigations.",
        "kshaya": "Kshaya (60th): Draining cycle; ending of old cycles, preparing for renewal."
    },

    // ── FESTIVALS DATABASE & RULES ──────────────────────────────────────────
    festivals: [
        // Ashadha
        { name: "Ashadha Navratri Begins", month: "Ashadha", paksha: "Shukla", tithi: "Pratipada", icon: "🌸" },
        { name: "Ishti", tithi: "Pratipada", icon: "🔥" },
        { name: "Chandra Darshana", paksha: "Shukla", tithi: "Pratipada", icon: "🌙" },
        { name: "Jagannath Rathyatra", month: "Ashadha", paksha: "Shukla", tithi: "Dwitiya", icon: "🚩" },
        { name: "Skanda Sashti", month: "Ashadha", paksha: "Shukla", tithi: "Shashthi", icon: "🔱" },
        { name: "Ashadha Ashtahnika Begins", month: "Ashadha", paksha: "Shukla", tithi: "Ashtami", icon: "🕉️" },
        { name: "Devshayani Ekadashi", month: "Ashadha", paksha: "Shukla", tithi: "Ekadashi", icon: "🛌" },
        { name: "Guru Purnima", month: "Ashadha", paksha: "Shukla", tithi: "Purnima", icon: "🎓" },
        { name: "Yogini Ekadashi", month: "Ashadha", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },

        // Shravana
        { name: "Hariyali Teej", month: "Shravana", paksha: "Shukla", tithi: "Tritiya", icon: "🌿" },
        { name: "Nag Panchami", month: "Shravana", paksha: "Shukla", tithi: "Panchami", icon: "🐍" },
        { name: "Shravana Putrada Ekadashi", month: "Shravana", paksha: "Shukla", tithi: "Ekadashi", icon: "🔱" },
        { name: "Varaha Jayanti", month: "Shravana", paksha: "Shukla", tithi: "Dwadashi", icon: "🐗" },
        { name: "Raksha Bandhan", month: "Shravana", paksha: "Shukla", tithi: "Purnima", icon: "🤝" },
        { name: "Kalki Jayanti", month: "Shravana", paksha: "Shukla", tithi: "Shashthi", icon: "🕉️" },
        { name: "Kamika Ekadashi", month: "Shravana", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },

        // Bhadrapada
        { name: "Kajari Teej", month: "Bhadrapada", paksha: "Krishna", tithi: "Tritiya", icon: "🌿" },
        { name: "Krishna Janmashtami", month: "Bhadrapada", paksha: "Krishna", tithi: "Ashtami", icon: "🍯" },
        { name: "Aja Ekadashi", month: "Bhadrapada", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },
        { name: "Ganesha Chaturthi", month: "Bhadrapada", paksha: "Shukla", tithi: "Chaturthi", icon: "🐘" },
        { name: "Radha Ashtami", month: "Bhadrapada", paksha: "Shukla", tithi: "Ashtami", icon: "🌸" },
        { name: "Parsva Ekadashi", month: "Bhadrapada", paksha: "Shukla", tithi: "Ekadashi", icon: "🔱" },
        { name: "Anant Chaturdashi", month: "Bhadrapada", paksha: "Shukla", tithi: "Chaturdashi", icon: "♾️" },
        { name: "Bhadrapada Purnima", month: "Bhadrapada", paksha: "Shukla", tithi: "Purnima", icon: "🌕" },

        // Ashwina
        { name: "Indira Ekadashi", month: "Ashwina", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },
        { name: "Sarvapitri Amavasya", month: "Ashwina", paksha: "Krishna", tithi: "Amavasya", icon: "🕊️" },
        { name: "Shardiya Navratri Begins", month: "Ashwina", paksha: "Shukla", tithi: "Pratipada", icon: "🔱" },
        { name: "Saraswati Avahan", month: "Ashwina", paksha: "Shukla", tithi: "Saptami", icon: "📖" },
        { name: "Durga Ashtami", month: "Ashwina", paksha: "Shukla", tithi: "Ashtami", icon: "🔱" },
        { name: "Maha Navami", month: "Ashwina", paksha: "Shukla", tithi: "Navami", icon: "🏹" },
        { name: "Dussehra", month: "Ashwina", paksha: "Shukla", tithi: "Dashami", icon: "🏹" },
        { name: "Papankusha Ekadashi", month: "Ashwina", paksha: "Shukla", tithi: "Ekadashi", icon: "🔱" },
        { name: "Kojagara Puja", month: "Ashwina", paksha: "Shukla", tithi: "Purnima", icon: "🌕" },

        // Kartika
        { name: "Karwa Chauth", month: "Kartika", paksha: "Krishna", tithi: "Chaturthi", icon: "🌙" },
        { name: "Ahoi Ashtami", month: "Kartika", paksha: "Krishna", tithi: "Ashtami", icon: "👶" },
        { name: "Rama Ekadashi", month: "Kartika", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },
        { name: "Dhanteras", month: "Kartika", paksha: "Krishna", tithi: "Trayodashi", icon: "🪙" },
        { name: "Narak Chaturdashi", month: "Kartika", paksha: "Krishna", tithi: "Chaturdashi", icon: "🪔" },
        { name: "Diwali", month: "Kartika", paksha: "Krishna", tithi: "Amavasya", icon: "🪔" },
        { name: "Govardhan Puja", month: "Kartika", paksha: "Shukla", tithi: "Pratipada", icon: "⛰️" },
        { name: "Bhai Dooj", month: "Kartika", paksha: "Shukla", tithi: "Dwitiya", icon: "🌸" },
        { name: "Chhath Puja", month: "Kartika", paksha: "Shukla", tithi: "Shashthi", icon: "☀️" },
        { name: "Devutthana Ekadashi", month: "Kartika", paksha: "Shukla", tithi: "Ekadashi", icon: "🔔" },
        { name: "Tulsi Vivah", month: "Kartika", paksha: "Shukla", tithi: "Dwadashi", icon: "🌿" },
        { name: "Kartik Purnima", month: "Kartika", paksha: "Shukla", tithi: "Purnima", icon: "🌕" },

        // Margashirsha
        { name: "Utpanna Ekadashi", month: "Margashirsha", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },
        { name: "Gita Jayanti", month: "Margashirsha", paksha: "Shukla", tithi: "Ekadashi", icon: "📖" },
        { name: "Dattatreya Jayanti", month: "Margashirsha", paksha: "Shukla", tithi: "Purnima", icon: "🕉️" },

        // Pausha
        { name: "Saphala Ekadashi", month: "Pausha", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },
        { name: "Pausha Putrada Ekadashi", month: "Pausha", paksha: "Shukla", tithi: "Ekadashi", icon: "🔱" },
        { name: "Shakambhari Purnima", month: "Pausha", paksha: "Shukla", tithi: "Purnima", icon: "🌕" },

        // Magha
        { name: "Shattila Ekadashi", month: "Magha", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },
        { name: "Mauni Amavasya", month: "Magha", paksha: "Krishna", tithi: "Amavasya", icon: "🤫" },
        { name: "Vasant Panchami", month: "Magha", paksha: "Shukla", tithi: "Panchami", icon: "🎻" },
        { name: "Jaya Ekadashi", month: "Magha", paksha: "Shukla", tithi: "Ekadashi", icon: "🔱" },
        { name: "Magha Purnima", month: "Magha", paksha: "Shukla", tithi: "Purnima", icon: "🌕" },

        // Phalguna
        { name: "Vijaya Ekadashi", month: "Phalguna", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },
        { name: "Maha Shivaratri", month: "Phalguna", paksha: "Krishna", tithi: "Chaturdashi", icon: "🕉️" },
        { name: "Amalaki Ekadashi", month: "Phalguna", paksha: "Shukla", tithi: "Ekadashi", icon: "🔱" },
        { name: "Holika Dahan", month: "Phalguna", paksha: "Shukla", tithi: "Chaturdashi", icon: "🔥" },
        { name: "Holi", month: "Phalguna", paksha: "Shukla", tithi: "Purnima", icon: "🎨" },

        // Chaitra
        { name: "Papmochani Ekadashi", month: "Chaitra", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },
        { name: "Chaitra Navratri Begins", month: "Chaitra", paksha: "Shukla", tithi: "Pratipada", icon: "🔱" },
        { name: "Gudi Padwa", month: "Chaitra", paksha: "Shukla", tithi: "Pratipada", icon: "🚩" },
        { name: "Gangaur", month: "Chaitra", paksha: "Shukla", tithi: "Tritiya", icon: "🌸" },
        { name: "Sri Rama Navami", month: "Chaitra", paksha: "Shukla", tithi: "Navami", icon: "🏹" },
        { name: "Kamada Ekadashi", month: "Chaitra", paksha: "Shukla", tithi: "Ekadashi", icon: "🔱" },
        { name: "Hanuman Jayanti", month: "Chaitra", paksha: "Shukla", tithi: "Purnima", icon: "🐒" },

        // Vaishakha
        { name: "Varuthini Ekadashi", month: "Vaishakha", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },
        { name: "Akshaya Tritiya", month: "Vaishakha", paksha: "Shukla", tithi: "Tritiya", icon: "💎" },
        { name: "Mohini Ekadashi", month: "Vaishakha", paksha: "Shukla", tithi: "Ekadashi", icon: "🔱" },
        { name: "Narasimha Jayanti", month: "Vaishakha", paksha: "Shukla", tithi: "Chaturdashi", icon: "🦁" },
        { name: "Buddha Purnima", month: "Vaishakha", paksha: "Shukla", tithi: "Purnima", icon: "🧘" },

        // Jyeshtha
        { name: "Apara Ekadashi", month: "Jyeshtha", paksha: "Krishna", tithi: "Ekadashi", icon: "🔱" },
        { name: "Shani Jayanti", month: "Jyeshtha", paksha: "Krishna", tithi: "Amavasya", icon: "⚖️" },
        { name: "Vat Savitri Vrat", month: "Jyeshtha", paksha: "Krishna", tithi: "Amavasya", icon: "🌳" },
        { name: "Ganga Dussehra", month: "Jyeshtha", paksha: "Shukla", tithi: "Dashami", icon: "🌊" },
        { name: "Nirjala Ekadashi", month: "Jyeshtha", paksha: "Shukla", tithi: "Ekadashi", icon: "🏺" },
        { name: "Vat Purnima Vrat", month: "Jyeshtha", paksha: "Shukla", tithi: "Purnima", icon: "🌳" }
    ],

    // Helper resolver to match rules dynamically
    getFestivalsForDay: function(lunarMonth, paksha, tithi, sunSign) {
        let matches = [];
        
        // Match specific rules
        this.festivals.forEach(rule => {
            // Normailze strings
            const mMatch = !rule.month || lunarMonth.toLowerCase().includes(rule.month.toLowerCase());
            const pMatch = !rule.paksha || paksha.toLowerCase().includes(rule.paksha.toLowerCase());
            const tMatch = !rule.tithi || tithi.toLowerCase().includes(rule.tithi.toLowerCase());
            
            if (mMatch && pMatch && tMatch) {
                matches.push({ name: rule.name, icon: rule.icon });
            }
        });

        // Match solar transits (Sankrantis)
        if (sunSign) {
            const transitRules = {
                "Mesha": { name: "Mesha Sankranti", icon: "♈" },
                "Vrishabha": { name: "Vrishabha Sankranti", icon: "♉" },
                "Mithuna": { name: "Mithuna Sankranti", icon: "♊" },
                "Karka": { name: "Karka Sankranti", icon: "♋" },
                "Simha": { name: "Simha Sankranti", icon: "♌" },
                "Kanya": { name: "Kanya Sankranti", icon: "♍" },
                "Tula": { name: "Tula Sankranti", icon: "♎" },
                "Vrishchika": { name: "Vrishchika Sankranti", icon: "♏" },
                "Dhanu": { name: "Dhanu Sankranti", icon: "♐" },
                "Makara": { name: "Makar Sankranti", icon: "♑" },
                "Kumbha": { name: "Kumbha Sankranti", icon: "♒" },
                "Meena": { name: "Meena Sankranti", icon: "♓" }
            };
            // Note: Since we compute calculations at 12:00, if Sun enters a sign, it's Sankranti today.
            // We can match it if transit happens on this day
        }

        return matches;
    }
};
