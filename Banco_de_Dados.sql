CREATE DATABASE loja_pure;
USE loja_pure;

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INT NOT NULL,
    categoria VARCHAR(200)
);

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    endereco TEXT
);

CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    produto_id INT,
    quantidade INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES 
('Blusa de Tricô', 'Blusa feminina de tricô artesanal', 120.00, 10, 'Roupas'),
('Perneira de Lã', 'Perneira feita à mão para o inverno', 60.00, 20, 'Roupas'),
('Brinco Turquesa', 'Brincos', 15.00, 5, 'Acessorios');

INSERT INTO clientes (nome, email, telefone, endereco) VALUES 
('Ana Silva', 'ana@gmail.com', '99999-9999', 'Rua das Flores, 123'),
('João Santos', 'joao@gmail.com', '88888-8888', 'Av. Central, 456'),
('Joana Darc', 'joana@gmail.com', '11800-666', 'Rua dez, 237');




