CREATE TABLE `cliente` (
   `id_cliente` INT,
   `nombre` VARCHAR(255) NOT NULL,
   `email` VARCHAR(255) NOT NULL,
   `telefono` INT NOT NULL,
   `direccion` VARCHAR(255) NOT NULL,
   PRIMARY KEY (`id_cliente`)
);

CREATE TABLE `pedido` (
   `id_pedidos` INT,
   `fecha_hora` DATETIME NOT NULL,
   `total` FLOAT NOT NULL,
   `id_cliente` INT NOT NULL,
   `id_metodo` INT NOT NULL,
   PRIMARY KEY (`id_pedidos`)
);

CREATE TABLE `pizza` (
   `id_pizza` INT,
   `nombre` VARCHAR(255) NOT NULL,
   `descripción` VARCHAR(255) NOT NULL,
   `precio_base` FLOAT NOT NULL,
   PRIMARY KEY (`id_pizza`)
);

CREATE TABLE `ingredientes` (
   `id_ingrediente` INT,
   `nombre` VARCHAR(255) NOT NULL,
   `precio` FLOAT NOT NULL,
   PRIMARY KEY (`id_ingrediente`)
);

CREATE TABLE `metodo_pago` (
   `id_metodo` INT,
   `tipo_pago` VARCHAR(255) NOT NULL,
   PRIMARY KEY (`id_metodo`)
);

CREATE TABLE `ingrediente_adicional` (
   `id_detalle` INT NOT NULL,
   `id_ingrediente` INT NOT NULL
   PRIMARY KEY ()
);

CREATE TABLE `detalle_pedido` (
   `id_detalle` INT,
   `cantidad` INT NOT NULL,
   `subtotal` FLOAT NOT NULL,
   `id_pedido` INT NOT NULL,
   `id_pizza` INT NOT NULL,
   PRIMARY KEY (`id_detalle`)
);


ALTER TABLE `pedido` ADD CONSTRAINT `FK_f6a354ec-e9c8-4476-bb34-c733c8937a61` FOREIGN KEY (`id_cliente`) REFERENCES `cliente`(`id_cliente`)  ;

ALTER TABLE `pedido` ADD CONSTRAINT `FK_abe5f8fa-03fb-4f3a-9079-ec2ffdd90283` FOREIGN KEY (`id_metodo`) REFERENCES `metodo_pago`(`id_metodo`)  ;

ALTER TABLE `ingrediente_adicional` ADD CONSTRAINT `FK_fc9853d6-9e82-4892-8d44-981471a59418` FOREIGN KEY (`id_detalle`) REFERENCES `detalle_pedido`(`id_detalle`)  ;

ALTER TABLE `ingrediente_adicional` ADD CONSTRAINT `FK_5dcf50ff-be63-4500-bd70-193c9b731fb6` FOREIGN KEY (`id_ingrediente`) REFERENCES `ingredientes`(`id_ingrediente`)  ;

ALTER TABLE `detalle_pedido` ADD CONSTRAINT `FK_090ee564-6a4f-4cc0-9688-ac0cc8cec0ba` FOREIGN KEY (`id_pedido`) REFERENCES `pedido`(`id_pedidos`)  ;

ALTER TABLE `detalle_pedido` ADD CONSTRAINT `FK_bc88a93c-48be-4e2a-9f5b-1dca20117822` FOREIGN KEY (`id_pizza`) REFERENCES `pizza`(`id_pizza`)  ;
