# Humming-Bird-2.0-UI
React-Redux based User Interface for revamped Humming Bird project

## Installation Instructions
This section details the steps required to install the required packages to run this project. If you have all the required packages, move to the next section.
If you have used default `create-react-app` it is advised you do these steps to understand each building block of the project.

0. Clone this repository into your projects folder and open the folder in terminal. 

1. You might want to use [nodeenv](https://ekalinin.github.io/nodeenv/) to create nodejs installation and thereby projects in local folder if you are not comfortable to install nodejs system wide.

2. Assuming you have nodejs installed, to install reactjs, in terminal run the command

`npm install react react-dom`

3. Next we will install `webpack` whose main purpose is to bundle all out code into a single minified file. Along with that we will install webpack-dev-server and webpack-cli.

`npm install --save-dev webpack webpack-dev-server webpack-cli`

4. Next we will install `babel`, which webpack requires to process ES6 code into ES5.

`npm install --save-dev @babel/core @babel/preset-env @babel/preset-react babel-loader @babel/plugin-proposal-class-properties`

5. We will install `eslint` next, which checks our code for any error or warning that can cause bugs.

`npm --save-dev install eslint eslint-loader babel-eslint eslint-config-react eslint-plugin-react`

Running `npm run eslint-fix` in this project will clear any lint errors for you. But it is advised you fix them yourselves and learn to write clean code.

6. Next, we install `LESS processor` which is a processor for style sheets.

`npm install --save-dev less less-loader css-loader style-loader`

7. We are all setup except we need to install `redux`. Run the following command to install redux and supporting libraries.

`npm install redux react-redux redux-thunk --save`

## Running the project
All the required configurations are preconfigured in the files in project directory. Following are the commands to run/configure the project.

0. `npm run start`

This command starts the server at `localhost:8080` and when ever a file is changed in project, the project is automatically built and the changes will reflect instantaneously in the browser.

1. `npm run build`

Will export the minified production version of the project to `build` folder in project home which has be hosted directly on a server.

2. `npm clean-install`

Will remove `node_modules` directory and reinstalls the required packages.

3. `npm install`

Will install listed packages that doesn't exist in `node_modules` folder. Run this command after the package you need is added in dependencies of `package.json`.

Commands for testing will be added once the test packages are configured.