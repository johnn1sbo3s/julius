FROM node:24-alpine

# Define diretório de trabalho
WORKDIR /app

# Copia package.json e package-lock.json
COPY package*.json ./

# Instala dependências como root
RUN npm install

# Copia o restante do código
COPY . .

# Ajusta permissões da pasta /app para o usuário node
RUN chown -R node:node /app

# Troca para o usuário node (já existe na imagem oficial com UID 1000)
USER node

# Expõe a porta do Vite
EXPOSE 5173

# Comando padrão
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
