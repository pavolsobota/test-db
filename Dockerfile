# Use an official Node.js runtime as a parent image
FROM node:14 AS node-stage

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the TypeScript code
RUN npm run build

# Use an official Python runtime as a parent image
FROM python:3.9 AS python-stage

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Python script from the node-stage
COPY --from=node-stage /usr/src/app /usr/src/app

# Install Python dependencies
RUN pip install pymongo pandas

# Final stage
FROM node:14

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Node.js application
COPY --from=node-stage /usr/src/app /usr/src/app

# Copy the Python dependencies
COPY --from=python-stage /usr/local/lib/python3.9 /usr/local/lib/python3.9

# Ensure Python is installed
RUN apt-get update && apt-get install -y python3 python3-pip

# Expose the port the app runs on
EXPOSE 3000

# Start the server
CMD ["npm", "start"]
