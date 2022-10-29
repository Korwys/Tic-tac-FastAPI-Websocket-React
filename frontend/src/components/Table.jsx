import React, {useState} from 'react';
import Board from "./Board";


let ws = new WebSocket("ws://localhost:8000/ws");
let currentPlayer = null;
let player = null;

export function Table() {

    const [info, setInfo] = useState('');
    const [playerName, setPlayerName] = useState('');
    const [currentPlayerName, setCurrentPlayerName] = useState('');

    let changePlayer = {
        "X": "O",
        "O": "X"
    }
    let rows = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [6, 4, 2],
        ]

    function updateCell(cell, player) {
        let getCell = document.getElementById(cell)
        getCell.innerHTML = player
    }

    function colorAllCells() {
        for (let c; c <= 9; c++)
            document.getElementById(c).style.background = 'grey'
    }

    function colorRow() {
        let cells = []
        for (let cell = 1; cell <= 10; cell++) {
            cells.push(document.getElementById(cell))
        }
        rows.forEach((row) => {
            console.log(row);
            if (cells[row[0]].innerHTML == cells[row[1]].innerHTML && cells[row[0]].innerHTML == cells[row[2]].innerHTML && cells[row[0]].innerHTML != "*") {
                console.log(cells[row[0]].innerHTML, cells[row[1]].innerHTML, cells[row[2]].innerHTML);
                cells[row[0]].style.backgroundColor = 'green';
                cells[row[1]].style.backgroundColor = 'green';
                cells[row[2]].style.backgroundColor = 'green';
            }
        });
    }

    function checkQueue() {
        currentPlayer = changePlayer[currentPlayer]
        if (player == currentPlayer) {
            setInfo('Your turn')
            setCurrentPlayerName(player)
        } else {
            setInfo("Your opponent's turn!")
            setCurrentPlayerName(changePlayer[player])
        }
    }

    ws.onmessage = (event) => {
        const response = JSON.parse(event.data)
        if (response.init) {
            setInfo(response.message)
            setPlayerName(response.player)
            if (response.message !== 'Awaiting second player') {
                player = response.player
            }
            currentPlayer = 'X'
            setCurrentPlayerName('X')

        } else if (response.info) {
            updateCell(response.cell, response.player)
            setInfo(' Sorry, but not today! You Lose!')

        } else {
            if (response.message === 'You Win') {
                console.log(response)
                updateCell(response.cell, response.player)
                setInfo(response.message)
                colorRow()
                ws.close(3001)
            } else if (response.message === 'Draw') {
                console.log(response)
                updateCell(response.cell, response.player)
                setInfo('It is Draw!')
                colorAllCells()
                ws.close(3001)
            } else {
                console.log(response)
                setInfo('Now your opponent turn')
                updateCell(response.cell, response.player)
                checkQueue()
            }
        }
    }
    return (
            <table className="table" id="main-table">
                <tr>
                    <td>
                        <h3>Tic Tac Round</h3>
                        <h4>Current player:{currentPlayerName} <span id="current-player"></span></h4>
                        <h3>You play by:{playerName}</h3> <span id="player"></span>
                        <h3>Info:{info}</h3> <span id="info"></span>
                    </td>
                    <Board player = {player} currentPlayer={currentPlayer} ws={ws}/>
                </tr>
            </table>
    );
};

export default ws;