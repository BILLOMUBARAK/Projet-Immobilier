CREATE DATABASE immobilier;
\c immobilier;

CREATE TABLE immeuble (
    id_immeuble SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    nomProprio VARCHAR(100),
    nbrEtage INTEGER,
    nbrAppart INTEGER,
    adresse VARCHAR(100)
);

CREATE TABLE appartement (
    id_appart SERIAL PRIMARY KEY,
    id_immeuble INTEGER REFERENCES immeuble(id_immeuble),
    noAppart INTEGER,
    noEtage INTEGER,
    type VARCHAR(100)
);

CREATE TABLE client (
    id_client SERIAL PRIMARY KEY,
    id_immeuble INTEGER REFERENCES immeuble(id_immeuble),
    id_appart INTEGER REFERENCES appartement(id_appart),
    nom VARCHAR(100),
    prenom VARCHAR(100),
    noAppart INTEGER
);

CREATE TABLE personnel (
    id_personnel SERIAL PRIMARY KEY,
    id_immeuble INTEGER REFERENCES immeuble(id_immeuble),
    nom VARCHAR(100),
    prenom VARCHAR(100)
);

CREATE TABLE paiementLoyer (
    id_paiement SERIAL PRIMARY KEY,
    id_immeuble INTEGER REFERENCES immeuble(id_immeuble),
    id_appart INTEGER REFERENCES appartement(id_appart),
    id_client INTEGER REFERENCES client(id_client),
    Montant FLOAT,
    date DATE,
    payer VARCHAR(3)
);
-- Insérer les données pour immeuble
INSERT INTO immeuble (id_immeuble, nom, nomProprio, nbrEtage, nbrAppart, adresse)
VALUES
    (46, 'Résidence Belle Vue', 'Gérard Lefevre', 5, 10, '15 Rue des Lilas, 75001 Paris'),
    (47, 'Le Château des Roses', 'Sophie Dupont', 4, 8, '8 Avenue Victor Hugo, 69002 Lyon'),
    (48, 'Les Jardins de la Rose', 'Pierre Martin', 6, 12, '23 Boulevard des Fleurs, 13008 Marseille'),
    (49, 'La Tour de la Cité', 'Claire Lambert', 7, 14, '12 Rue du Commerce, 31000 Toulouse'),
    (55, 'Les Terrasses du Lac', 'Lucie Bernard', 5, 10, '5 Quai de la République, 44000 Nantes'),
    (51, 'Le Domaine des Cerisiers', 'Marc Dubois', 4, 8, '10 Rue des Cerisiers, 67000 Strasbourg'),
    (52, 'Résidence Harmonie', 'Nathalie Robert', 6, 12, '18 Rue du Paradis, 59000 Lille'),
    (53, 'Les Hauts de la Colline', 'Philippe Renard', 7, 14, '9 Avenue de la Liberté, 21000 Dijon'),
    (54, 'La Villa du Soleil', 'Isabelle Petit', 5, 10, '3 Rue du Soleil, 38000 Grenoble');

-- Insérer les données pour appartement
INSERT INTO appartement (id_appart, id_immeuble, noAppart, noEtage, type)
VALUES
    (101, 46, 1, 1, 'Appartement A1'),
    (102, 47, 2, 1, 'Appartement B1'),
    (103, 48, 3, 1, 'Appartement C1'),
    (104, 49, 4, 1, 'Appartement D1'),
    (105, 55, 5, 1, 'Appartement E1'),
    (106, 51, 6, 1, 'Appartement F1'),
    (107, 52, 7, 1, 'Appartement G1'),
    (108, 53, 8, 1, 'Appartement H1'),
    (109, 54, 9, 1, 'Appartement I1'),
    (110, 55, 10, 1, 'Appartement J1');

-- Insérer les données pour client
INSERT INTO client (id_client, id_immeuble, id_appart, nom, prenom, noAppart)
VALUES
    (23, 46, 101, 'Client 1', 'Prénom 1', 1),
    (24, 47, 102, 'Client 2', 'Prénom 2', 2),
    (25, 48, 103, 'Client 3', 'Prénom 3', 3),
    (26, 49, 104, 'Client 4', 'Prénom 4', 4),
    (27, 55, 105, 'Client 5', 'Prénom 5', 5),
    (28, 51, 106, 'Client 6', 'Prénom 6', 6),
    (29, 52, 107, 'Client 7', 'Prénom 7', 7),
    (30, 53, 108, 'Client 8', 'Prénom 8', 8),
    (31, 54, 109, 'Client 9', 'Prénom 9', 9),
    (32, 55, 110, 'Client 10', 'Prénom 10', 10);

-- Insérer les données pour personnel (exemples fictifs)
INSERT INTO personnel (id_personnel, id_immeuble, nom, prenom)
VALUES
    (1, 46, 'Personnel 1', 'Prénom 1'),
    (2, 47, 'Personnel 2', 'Prénom 2'),
    (3, 48, 'Personnel 3', 'Prénom 3'),
    (4, 49, 'Personnel 4', 'Prénom 4'),
    (5, 55, 'Personnel 5', 'Prénom 5'),
    (6, 51, 'Personnel 6', 'Prénom 6'),
    (7, 52, 'Personnel 7', 'Prénom 7'),
    (8, 53, 'Personnel 8', 'Prénom 8'),
    (9, 54, 'Personnel 9', 'Prénom 9'),
    (10, 55, 'Personnel 10', 'Prénom 10');

-- Insérer les données initiales pour la classe paiementLoyer
INSERT INTO paiementLoyer (id_immeuble, id_appart, id_client, Montant, date, payer)
VALUES
    (46, 101, 23, 500.0, '2024-01-15', 'oui'),
    (47, 102, 24, 450.0, '2024-02-16', 'non'),
    (48, 103, 25, 600.0, '2024-03-17', 'oui'),
    (49, 104, 26, 550.0, '2024-04-18', 'non'),
    (55, 105, 27, 700.0, '2024-05-19', 'oui'),
    (51, 106, 28, 650.0, '2024-06-20', 'non'),
    (52, 107, 29, 800.0, '2024-07-21', 'oui'),
    (53, 108, 30, 750.0, '2024-08-22', 'non'),
    (54, 109, 31, 900.0, '2024-09-23', 'oui'),
    (55, 110, 32, 850.0, '2024-10-24', 'non');
