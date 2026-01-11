import subprocess
import sys
import os


def png_to_fen(image_path):
    """
    convert png to FEN using tensorflow-chessbot from local repo

    args:
        image_path: path to chessboard image

    returns:
        dict with 'success', 'fen', 'certainty', or 'error'
    """
    # file paths (CHANGE TCB_DIR TO WHATEVER IT WILL BE SAVED AS)
    tcb_dir = os.path.abspath('./tensorflow_chessbot')
    image_path = os.path.abspath(image_path)

    # run tensorflow-chessbot
    result = subprocess.run(
        [sys.executable, 'tensorflow_chessbot.py', '--filepath', image_path],
        capture_output=True,
        text=True,
        cwd=tcb_dir
    )

    # parse output
    if result.returncode != 0:
        return {
            'success': False,
            'error': result.stderr.strip() if result.stderr else 'unknown error',
            'stdout': result.stdout
        }

    # find fen and certainty
    lines = result.stdout.split('\n')
    fen = None
    certainty = None

    for i, line in enumerate(lines):
        if 'Predicted FEN:' in line:
            if i + 1 < len(lines):
                fen = lines[i + 1].strip()
                # whitespace nuker
                if fen.startswith('---'):
                    fen = None
                elif fen:
                    # fen might have gamestate info just take pos
                    pass

        if 'Final Certainty:' in line:
            try:
                certainty = float(line.split('Final Certainty:')[1].strip().replace('%', ''))
            except:
                pass

    if fen:
        return {'success': True, 'fen': fen, 'certainty': certainty}
    else:
        return {
            'success': False,
            'error': 'no FEN found in output',
            'stdout': result.stdout
        }


def png_to_fen_url(url):
    """
    convert image URL to FEN using tensorflow-chessbot
    
    args:
        url: URL to chessboard image

    returns:
        dict with 'success', 'fen', 'certainty', or 'error'
    """
    tcb_dir = os.path.abspath('./tensorflow_chessbot')

    result = subprocess.run(
        [sys.executable, 'tensorflow_chessbot.py', '--url', url],
        capture_output=True,
        text=True,
        cwd=tcb_dir
    )

    if result.returncode != 0:
        return {
            'success': False,
            'error': result.stderr.strip() if result.stderr else 'unknown error',
            'stdout': result.stdout
        }

    # extract FEN and certainty
    lines = result.stdout.split('\n')
    fen = None
    certainty = None

    for i, line in enumerate(lines):
        if 'Predicted FEN:' in line:
            if i + 1 < len(lines):
                fen = lines[i + 1].strip()
                if fen.startswith('---'):
                    fen = None

        if 'Final Certainty:' in line:
            try:
                certainty = float(line.split('Final Certainty:')[1].strip().replace('%', ''))
            except:
                pass

    if fen:
        return {'success': True, 'fen': fen, 'certainty': certainty}
    else:
        return {
            'success': False,
            'error': 'no FEN found in output',
            'stdout': result.stdout
        }



if __name__ == '__main__':
    #test with png
    result = png_to_fen('chessboard.png')
    if result['success']:
        print(f"FEN: {result['fen']}")
        print(f"Certainty: {result['certainty']}%")
    else:
        print(f"Error: {result['error']}")

    #test with URL
    result = png_to_fen_url('http://imgur.com/u4zF5Hj.png')
    if result['success']:
        print(f"FEN: {result['fen']}")
        print(f"Certainty: {result['certainty']}%")
