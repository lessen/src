

def atom(x)  :
  try: return int(x)
  except:
    try: return float(x)
    except ValueError:
      return x
