-- Platform
CREATE TABLE platform(
   id INT,
   name VARCHAR(250) NOT NULL,
   abbreviation VARCHAR(100),
   summary TEXT,
   slug VARCHAR(50),
   entreprise VARCHAR(50),
   generation INT,
   category INT,
   family INT,
   type INT,
   alternative_name VARCHAR(250),
   PRIMARY KEY(id)
);

-- Game Category
CREATE TABLE game_category(
   id INT,
   name VARCHAR(50),
   PRIMARY KEY(id)
);

-- Platform  Version
CREATE TABLE platform_version(
   id INT,
   version_name VARCHAR(50),
   PRIMARY KEY(id)
);

-- Player Perspective
CREATE TABLE player_perspective(
   id INT,
   name VARCHAR(50),
   slug VARCHAR(50),
   PRIMARY KEY(id)
);


-- Game Engines
CREATE TABLE game_engines(
   id INT,
   name VARCHAR(150),
   slug VARCHAR(150),
   description TEXT,
   PRIMARY KEY(id)
);

-- Age Ratings
CREATE TABLE age_ratings(
   id INT,
   organization VARCHAR(50),
   age VARCHAR(50),
   PRIMARY KEY(id)
);

-- Multiplayer Modes
CREATE TABLE multiplayer_modes(
   id INT,
   campaigncoop BOOLEAN NOT NULL,
   lancoop BOOLEAN,
   offlinecoop BOOLEAN,
   offlinecoopmax SMALLINT,
   offlinemax SMALLINT,
   onlinecoop BOOLEAN,
   onlinecoopmax SMALLINT,
   onlinemax SMALLINT,
   platform_id  INT,
   splitscreen BOOLEAN,
   splitscreenonline BOOLEAN,
   PRIMARY KEY(id)
);

-- Company Status
CREATE TABLE company_status(
   id INT,
   name VARCHAR(100),
   PRIMARY KEY(id)
);

-- Game Engine Logos
CREATE TABLE game_engine_logos(
   id INT,
   url TEXT,
   PRIMARY KEY(id)
);

-- Game
CREATE TABLE game(
   id INT,
   name VARCHAR(100) NOT NULL,
   slug VARCHAR(100) NOT NULL,
   summary TEXT,
   first_release_date DATE,
   total_rating DECIMAL(5,2),
   PRIMARY KEY(id)
);

-- Language Supports
CREATE TABLE language_supports(
   id INT,
   language_id SMALLINT,
   language_support_type_id SMALLINT,
   game_id INT,
   PRIMARY KEY(id),
   FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE
);

-- Language
CREATE TABLE language(
   id INT,
   locale VARCHAR(100),
   name VARCHAR(250),
   native_name VARCHAR(250),
   PRIMARY KEY(id)
);

-- Languague Support Types
CREATE TABLE language_supports_type(
   id INT,
   name VARCHAR(50),
   PRIMARY KEY(id)
);

-- Genres
CREATE TABLE genres (
   id INT,
   name VARCHAR(100),
   PRIMARY KEY(id)
);

-- Videos
CREATE TABLE videos(
   id INT PRIMARY KEY,
   game_id INT,
   name VARCHAR(200),
   video_id VARCHAR(150),
   FOREIGN KEY(game_id) REFERENCES game(id) ON DELETE CASCADE
);

-- Company
CREATE TABLE company(
   id INT,
   changed_company_id INT,
   country VARCHAR(250),
   description TEXT,
   name VARCHAR(250),
   parent INT,
   slug VARCHAR(250),
   start_date DATE,
   status_id INT,
   PRIMARY KEY(id),
   FOREIGN KEY (parent) REFERENCES company(id) ON DELETE CASCADE
);

-- Company Logos
CREATE TABLE company_logos(
   id INT,
   url TEXT,
   PRIMARY KEY(id)
);


-- Jeu / Platform (avec prix optionnel)
CREATE TABLE game_platform (
    game_id INT,
    platform_id INT,
    platform_price VARCHAR(50),
    PRIMARY KEY (game_id, platform_id),
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (platform_id) REFERENCES platform(id) ON DELETE CASCADE
);

-- Platform / Version
CREATE TABLE platform_platform_version (
    platform_id INT,
    version_id INT,
    PRIMARY KEY (platform_id, version_id),
    FOREIGN KEY (platform_id) REFERENCES platform(id) ON DELETE CASCADE,
    FOREIGN KEY (version_id) REFERENCES platform_version(id) ON DELETE CASCADE
);

-- Jeu / Catégorie
CREATE TABLE game_game_category (
    game_id INT,
    category_id INT,
    PRIMARY KEY (game_id, category_id),
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES game_category(id) ON DELETE CASCADE
);

-- Jeu / Genre
CREATE TABLE game_genre (
    game_id INT,
    genre_id INT,
    PRIMARY KEY (game_id, genre_id),
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
);

-- Jeu / Game Engine
CREATE TABLE game_game_engine (
    game_id INT,
    engine_id INT,
    PRIMARY KEY (game_id, engine_id),
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (engine_id) REFERENCES game_engines(id) ON DELETE CASCADE
);

-- Jeu / Perspective Joueur
CREATE TABLE game_player_perspective (
    game_id INT,
    perspective_id INT,
    PRIMARY KEY (game_id, perspective_id),
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (perspective_id) REFERENCES player_perspective(id) ON DELETE CASCADE
);

-- Jeu / Vidéos
CREATE TABLE game_video (
    game_id INT,
    video_id INT,
    PRIMARY KEY (game_id, video_id),
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE
);

-- Jeu / Age Rating
CREATE TABLE game_age_rating (
    game_id INT,
    age_rating_id INT,
    PRIMARY KEY (game_id, age_rating_id),
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (age_rating_id) REFERENCES age_ratings(id) ON DELETE CASCADE
);

-- Jeu / Modes Multijoueurs
CREATE TABLE game_multiplayer_mode (
    game_id INT,
    multiplayer_mode_id INT,
    PRIMARY KEY (game_id, multiplayer_mode_id),
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (multiplayer_mode_id) REFERENCES multiplayer_modes(id) ON DELETE CASCADE
);

-- Platform / Modes Multijoueurs
CREATE TABLE platform_multiplayer_mode (
    platform_id INT,
    multiplayer_mode_id INT,
    PRIMARY KEY (platform_id, multiplayer_mode_id),
    FOREIGN KEY (platform_id) REFERENCES platform(id) ON DELETE CASCADE,
    FOREIGN KEY (multiplayer_mode_id) REFERENCES multiplayer_modes(id) ON DELETE CASCADE
);

-- Jeu / Supports Langues
CREATE TABLE game_language_support (
    game_id INT,
    language_support_id INT,
    PRIMARY KEY (game_id, language_support_id),
    FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE,
    FOREIGN KEY (language_support_id) REFERENCES language_supports(id) ON DELETE CASCADE
);

-- Language support / Language
CREATE TABLE language_support_language (
    language_support_id INT,
    language_id INT,
    PRIMARY KEY (language_support_id, language_id),
    FOREIGN KEY (language_support_id) REFERENCES language_supports(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id) REFERENCES language(id) ON DELETE CASCADE
);

-- Language support / Type de support
CREATE TABLE language_support_language_support_type (
    language_support_id INT,
    support_type_id INT,
    PRIMARY KEY (language_support_id, support_type_id),
    FOREIGN KEY (language_support_id) REFERENCES language_supports(id) ON DELETE CASCADE,
    FOREIGN KEY (support_type_id) REFERENCES language_supports_type(id) ON DELETE CASCADE
);

-- Company / Game Engine
CREATE TABLE company_game_engine (
    company_id INT,
    engine_id INT,
    PRIMARY KEY (company_id, engine_id),
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (engine_id) REFERENCES game_engines(id) ON DELETE CASCADE
);

-- Company / Company Status (si besoin)
CREATE TABLE company_company_status (
    company_id INT,
    status_id INT,
    PRIMARY KEY (company_id, status_id),
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES company_status(id) ON DELETE CASCADE
);

-- Company / Logo
CREATE TABLE company_logo (
    company_id INT,
    logo_id INT,
    PRIMARY KEY (company_id, logo_id),
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (logo_id) REFERENCES company_logos(id) ON DELETE CASCADE
);

-- Game Engine / Logo
CREATE TABLE game_engine_logo (
    engine_id INT,
    logo_id INT,
    PRIMARY KEY (engine_id, logo_id),
    FOREIGN KEY (engine_id) REFERENCES game_engines(id) ON DELETE CASCADE,
    FOREIGN KEY (logo_id) REFERENCES game_engine_logos(id) ON DELETE CASCADE
);

-- Company published (self join)
CREATE TABLE company_published_by (
    company_id INT,
    publisher_id INT,
    PRIMARY KEY (company_id, publisher_id),
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (publisher_id) REFERENCES company(id) ON DELETE CASCADE
);

-- Company developed (self join)
CREATE TABLE company_developed_by (
    company_id INT,
    developer_id INT,
    PRIMARY KEY (company_id, developer_id),
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (developer_id) REFERENCES company(id) ON DELETE CASCADE
);
