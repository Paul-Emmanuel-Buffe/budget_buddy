create database banque;

CREATE TABLE Utilisateur(
        idUtilisateur Int  Auto_increment  NOT NULL ,
        nom           Varchar (50) NOT NULL ,
        prenom        Varchar (50) NOT NULL ,
        email         Varchar (100) NOT NULL ,
        motDePasse    Varchar (50) NOT NULL ,
        admin         Bool NOT NULL
	,CONSTRAINT Utilisateur_PK PRIMARY KEY (idUtilisateur)
);
CREATE TABLE type(
        idType Int  Auto_increment  NOT NULL ,
        titre  Varchar (100) NOT NULL
	,CONSTRAINT type_PK PRIMARY KEY (idType)
);
CREATE TABLE categorie(
        idCategorie Int  Auto_increment  NOT NULL ,
        titre       Varchar (200) NOT NULL
	,CONSTRAINT categorie_PK PRIMARY KEY (idCategorie)
);
CREATE TABLE compte(
        idCompte      Int  Auto_increment  NOT NULL ,
        montant       Float NOT NULL ,
        idUtilisateur Int NOT NULL
	,CONSTRAINT compte_PK PRIMARY KEY (idCompte)
	,CONSTRAINT compte_Utilisateur_FK FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur)
);
CREATE TABLE Transaction(
        reference       Int  Auto_increment  NOT NULL ,
        description     Varchar (250) NOT NULL ,
        montant         Float NOT NULL ,
        dateTransaction Date NOT NULL ,
        idCategorie     Int NOT NULL ,
        idType          Int NOT NULL ,
        idCompte        Int NOT NULL
	,CONSTRAINT Transaction_PK PRIMARY KEY (reference)
	,CONSTRAINT Transaction_categorie_FK FOREIGN KEY (idCategorie) REFERENCES categorie(idCategorie)
	,CONSTRAINT Transaction_type0_FK FOREIGN KEY (idType) REFERENCES type(idType)
	,CONSTRAINT Transaction_compte1_FK FOREIGN KEY (idCompte) REFERENCES compte(idCompte)
);

