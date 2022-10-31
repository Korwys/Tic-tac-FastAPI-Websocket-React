import React from 'react';

export function Board(props) {

    function checkCell(cell) {
        if (cell.innerHTML == '*' && props.player == props.currentPlayer) {
            return true
        } else {
            return false
        }
    }

    function cellClick(id) {
        let cell = document.getElementById(id)
        if (checkCell(cell)) {
            props.ws.send(JSON.stringify({player: props.player, cell: id}))
        } else {
            props.setInfo('Now not is your turn or Choose another cell')
        }
    }
    return (
            <td className="board-cell" id="board-cell">
                <div className='name'>
                    <table id="board">
                        <tr>
                            <td id="1" onClick={() => {cellClick(1)}}>*</td>
                            <td id="2" onClick={() => {cellClick(2)}}>*</td>
                            <td id="3" onClick={() => {cellClick(3)}}>*</td>
                        </tr>
                        <tr>
                            <td id="4" onClick={() => {cellClick(4)}}>*</td>
                            <td id="5" onClick={() => {cellClick(5)}}>*</td>
                            <td id="6" onClick={() => {cellClick(6)}}>*</td>
                        </tr>
                        <tr>
                            <td id="7" onClick={()=>{cellClick(7)}}>*</td>
                            <td id="8" onClick={()=>{cellClick(8)}}>*</td>
                            <td id="9" onClick={()=> {cellClick(9)}}>*</td>
                        </tr>
                    </table>
                </div>
            </td>
    );
}

export default Board;