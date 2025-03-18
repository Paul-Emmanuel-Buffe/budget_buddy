


insert into categorie (titre) 
values ("loisir"),("finance"),("autres")

insert into type (titre) 
values ("retrait"),("versement"),("virement")



insert into utilisateur (nom, prenom, email, motDePasse, admin)
values ("chevalier", "alexandre","alexandre.chevalier@blabla.fr", "Alexandre2193.", False),
("buffe", "paul","paul.buffe@blabla.fr", "Paulembu123/", False),
("fumey", "sewa","sewa.fumey@blabla.fr", "Sewa213/ad", True);

















####################################################################################
                    algo pour hasher le mot de passe
####################################################################################
import hashlib;
import secrets

salt = secrets.token_hex(16)

password = input("Enter your password: ")

hash_object = hashlib.sha256((password + salt).encode())

hash_hex = hash_object.hexdigest()

######################################################################################

######################################################################################

