# SC18IM700 Python library


## Document


## How to install

- Install directly with `pip` command  

  ```sh
  pip install "git+ssh://github.com/y2kblog/sc18im700-py.git"
  ```

- Install from `requirements.txt`  
  If you install with `pip install -r requirements.txt`, put the following in `requirements.txt`
  ```txt
  -e "git+ssh://github.com/y2kblog/sc18im700-py.git#egg=sc18im700"
  ```

After installing the package, it can be imported with the following command.  
```python
import sc18im700
```

## Getting Started

```python
import sys
from sc18im700 import SC18IM700

if __name__ == "__main__":
    sc18 = SC18IM700(port='COM7', baudrate=9600)
    dev_addr_list = sc18.i2c_device_search()
    if len(dev_addr_list) == 0:
        sys.exit(1)

    i2c_addr = dev_addr_list[0]
    sc18.set_defalt_i2c_addr(i2c_addr)
    print(sc18.i2c_mem_read(reg_addr=0x03, size=4))
```
