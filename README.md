<h1 align="center" style="font-weight: bold; font-family: Lato; ">ChessAR - Server</h1>

<p align="center">
 <a href="#pre">Technologies</a> •
 <a href="#started">Getting Started</a> •
 <a href="#colab">Collaborators</a>
</p>

<p align="center">
    <b>The main backend solution for the ChessAR Glasses</b>
    <p>ChessAR is a project dedicated to helping players make the best decision possible during a game of chess without having to insert something up their... well, bum. Just wear the glasses and voila, you have a chess master right in front of your eyes!
It's so easy it almost feels like cheating... because, let's be honest, it kind of is! But hey, nobody needs to know your secret weapon.

Why struggle with chess strategy when you can have grandmaster moves beamed directly to your eyeballs?
</p>
</p>

<h2 id="pre">Prerequisites</h2>
You need Python 3.11 < for a stable version of the project. You can download it from the official website.
<h3>Application</h3>

 <a href="https://python.org">Python</a><br/>

<h2 id="started">🚀 Getting started</h2>

<h3>Cloning</h3>

How to clone this project

```bash
git clone git@github.com:CogitoNTNU/ChessAR-Server.git
```

<h3>Starting</h3>

To setup and install all the dependencies of the project:

```bash
cd ChessAR-Server
./setup.sh
```

Then we can run the main application:

```bash
python src/main.py
```

<h3>Testing</h3>
Using pytest, we can run all the tests in the project by running:

```bash
pytest
```

be sure to do this in the root directory of the project.

<h2 id="#gen">General</h2>

This repository is only a part of the solution. This is the backend that is going to communicate with the IOT smart glasses. The main idea is that the chess glasses sends the viewport in binary to the server, and the server takes on the rest of the challenge to predict the best move for the player. The server will then send the move back to the glasses, and the player can make the move on the board.

<h3>Roadmap</h3>
<img src="./docs/images/strategy.png " alt="Roadmap" style="width: 100%;"/>

<h3>Architecture</h3>
... TODO!


<h2 id="colab">🤝 Collaborators</h2>

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/74411800?v=4" width="100px;" alt="Simon Sandvik Lee"/><br>
        <sub>
          <b>Simon Sandvik Lee - Lead</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/111222086?v=4" width="100px;" alt="Alice Zheng"/><br>
        <sub>
          <b>Alice Zheng - Member</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <im src="https://avatars.githubusercontent.com/u/105772595?v=4" width="100px;" alt="Vetle Støren"/><br>
        <sub>
          <b>Vetle Støren - Member</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/92276108?v=4" width="100px;" alt="Håkon Støren"/><br>
        <sub>
          <b>Håkon Støren - Member</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/77111032?v=4" width="100px;" alt="Jessica Liu"/><br>
        <sub>
          <b>Jessica Liu - Member</b>
        </sub>
      </a>
    </td>
  </tr>
</table>
