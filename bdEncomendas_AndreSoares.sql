CREATE DATABASE bdencomendas_T1;

USE bdencomendas_T1;

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

INSERT INTO `cliente`(`id`,`nome`,`email`,`telefone`,`nif`,`morada`) VALUES(1,'Lourenço Carneiro','lourencohomosexual@gaymail.pt','+351 969696969',111111111,'Rotunda da Boavista');
INSERT INTO `cliente`(`id`,`nome`,`email`,`telefone`,`nif`,`morada`) VALUES(2,'Gonçalo Moreira','ilovegothmommies@yahoo.pt','+256 912648955',998800712,'Cabanas de Goblins');
INSERT INTO `cliente`(`nome`,`telefone`,`email`,`morada`,`id`,`nif`) VALUES('Leonardo Raposo','+351 919826583','ilovemyhorsedaddy@yahoo.com','Cemitério de Águas Santas',3,222222222);

INSERT INTO `categoria`(`id`,`designacao`) VALUES(1,'Frágil');
INSERT INTO `categoria`(`id`,`designacao`) VALUES(2,'Cavalo');
INSERT INTO `categoria`(`id`,`designacao`) VALUES(3,'Pesadas');

INSERT INTO `artigo`(`id`,`idCategoria`,`designacao`,`stock`,`preco`) VALUES(1,2,'Cavalo do LeoFox',1,0);
INSERT INTO `artigo`(`id`,`idCategoria`,`designacao`,`preco`,`stock`) VALUES(2,1,'Lourenço',100000,1);
INSERT INTO `artigo`(`designacao`,`id`,`idCategoria`,`preco`,`stock`) VALUES('EGO DO LOURENCO CARNEIRO',3,3,99999999,0);

INSERT INTO `encomenda`(`nEncomenda`,`idCliente`,`dataEncomenda`,`dataEntrega`) VALUES(1,2,'2023-09-11','2025-11-24');
INSERT INTO `encomenda`(`nEncomenda`,`idCliente`,`dataEncomenda`,`dataEntrega`) VALUES(2,3,'2025-05-22','2025-11-24');
INSERT INTO `encomenda`(`nEncomenda`,`idCliente`,`dataEncomenda`,`dataEntrega`) VALUES(3,1,'2025-11-23','2025-11-24');

INSERT INTO `detalheencomenda`(`nEncomenda`,`idArtigo`,`quantidade`) VALUES(1,2,1);
INSERT INTO `detalheencomenda`(`nEncomenda`,`idArtigo`,`quantidade`) VALUES(2,1,1);
INSERT INTO `detalheencomenda`(`nEncomenda`,`idArtigo`,`quantidade`) VALUES(3,3,1);