 INSERT INTO utilisateur (nom, prenom, email, motDePasse, admin)
VALUES
    -> ('Dupont', 'Alice', 'alice.dupont@mail.com', 'mdp123', 1),
    -> ('Martin', 'Bob', 'bob.martin@mail.com', 'secret', 0),
    -> ('Leroy', 'Clara', 'clara.leroy@mail.com', 'clara2023', 0),
    -> ('Dubois', 'David', 'david.dubois@mail.com', 'dubois456', 1),
    -> ('Roux', 'Emma', 'emma.roux@mail.com', 'emma789', 0);

INSERT INTO categorie (titre)
    -> VALUES
    -> ('Alimentation'),
    -> ('Salaire'),
    -> ('Loyer'),
    -> ('Factures'),
    -> ('Loisirs');

INSERT INTO type (titre)
    -> VALUES
    -> ('Revenu'),
    -> ('Dépense');   

 INSERT INTO compte (montant, idUtilisateur)
    -> VALUES
    -> (1500.00, 1),   -- Compte d'Alice (admin)
    -> (3000.00, 2),   -- Compte de Bob
    -> (4500.00, 3),   -- Compte de Clara
    -> (200.50, 4),    -- Compte de David (admin)
    -> (7500.75, 5),   -- Compte d'Emma
    -> (1000.00, 1),   -- 2ème compte d'Alice
    -> (500.00, 2),    -- 2ème compte de Bob
    -> (3200.00, 3);   -- 2ème compte de Clara

 INSERT INTO transaction (description, montant, dateTransaction, idCategorie, idType, idCompte)
    -> VALUES
    -> ('Salaire Octobre', 2000.00, '2023-10-01', 2, 1, 1),     -- Revenu (Salaire)
    -> ('Courses Carrefour', -120.50, '2023-10-05', 1, 2, 1),   -- Dépense (Alimentation)
    -> ('Loyer Appartement', -700.00, '2023-11-01', 3, 2, 2),    -- Dépense (Loyer)
    -> ('Facture EDF', -85.30, '2023-10-15', 4, 2, 3),           -- Dépense (Factures)
    -> ('Vente Ebay', 300.00, '2023-10-20', 5, 1, 4),            -- Revenu (Loisirs)
    -> ('Cinéma Pathé', -25.00, '2023-10-12', 5, 2, 1),          -- Dépense (Loisirs)
    -> ('Prime Performance', 500.00, '2023-11-05', 2, 1, 5),     -- Revenu (Salaire)
    -> ('Restaurant Sushi', -45.90, '2023-10-08', 1, 2, 2),      -- Dépense (Alimentation)
    -> ('Achat Bureau', -350.75, '2023-11-10', 5, 2, 3),         -- Dépense (Loisirs)
    -> ('Remboursement', 150.00, '2023-10-25', 5, 1, 4);         -- Revenu (Loisirs)
     -> ('Courses Carrefour', -95.30, '2023-10-07', 1, 2, 3),      -- Alimentation (Dépense)
    -> ('Salaire Novembre', 2200.00, '2023-11-01', 2, 1, 3),     -- Salaire (Revenu)
    -> ('Loyer Appartement', -800.00, '2023-10-05', 3, 2, 3),     -- Loyer (Dépense)
    -> ('Facture Internet', -45.90, '2023-10-18', 4, 2, 3),       -- Factures (Dépense)
    -> ('Cinéma', -15.00, '2023-11-10', 5, 2, 3),                 -- Loisirs (Dépense)
    -> ('Vente livres', 75.00, '2023-10-22', 5, 1, 3),            -- Loisirs (Revenu)
    -> ('Super U', -62.40, '2023-11-05', 1, 2, 3);                -- Alimentation (Dépense);