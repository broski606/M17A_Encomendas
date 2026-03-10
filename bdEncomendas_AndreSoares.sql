CREATE DATABASE bdEncomendas_T1;

USE bdEncomendas_T1;

CREATE TABLE categoria(
id INT PRIMARY KEY,
designacao VARCHAR(50) NOT NULL
)engine=innodb;

CREATE TABLE artigo(id INT PRIMARY KEY, 
idCategoria INT, 
designacao VARCHAR(50) NOT NULL, 
preco DECIMAL(10,2), stock INT, 
FOREIGN KEY (idCategoria) REFERENCES categoria(id) ON UPDATE CASCADE ON DELETE CASCADE
)engine=innodb;

CREATE TABLE cliente(
id INT PRIMARY KEY,
nome VARCHAR(50) NOT NULL,
morada VARCHAR(100) NOT NULL,
telefone VARCHAR(15) NOT NULL,
email VARCHAR(50) NOT NULL,
nif INT
)engine=innodb;

CREATE TABLE encomenda(
nEncomenda INT PRIMARY KEY,
idCliente INT,
dataEncomenda DATE,
dataEntrega DATE,
FOREIGN KEY (idCliente) REFERENCES cliente(id) ON UPDATE CASCADE ON DELETE CASCADE
)engine=innodb;

CREATE TABLE detalheencomenda(
nEncomenda INT NOT NULL,
idArtigo INT NOT NULL,
quantidade INT,
PRIMARY KEY (nEncomenda, idArtigo),
FOREIGN KEY (nEncomenda) REFERENCES encomenda(nEncomenda) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (idArtigo) REFERENCES artigo(id) ON UPDATE CASCADE ON DELETE CASCADE
)engine=innodb;
