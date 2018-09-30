/**
 * This file was generated from grammar.peg
 * See http://canopy.jcoglan.com/ for documentation.
 */

(function() {
  'use strict';

  var extend = function(destination, source) {
    if (!destination || !source) return destination;
    for (var key in source) {
      if (destination[key] !== source[key])
        destination[key] = source[key];
    }
    return destination;
  };

  var formatError = function(input, offset, expected) {
    var lines = input.split(/\n/g),
        lineNo = 0,
        position = 0;

    while (position <= offset) {
      position += lines[lineNo].length + 1;
      lineNo += 1;
    }
    var message = 'Line ' + lineNo + ': expected ' + expected.join(', ') + '\n',
        line = lines[lineNo - 1];

    message += line + '\n';
    position -= line.length + 1;

    while (position < offset) {
      message += ' ';
      position += 1;
    }
    return message + '^';
  };

  var inherit = function(subclass, parent) {
    var chain = function() {};
    chain.prototype = parent.prototype;
    subclass.prototype = new chain();
    subclass.prototype.constructor = subclass;
  };

  var TreeNode = function(text, offset, elements) {
    this.text = text;
    this.offset = offset;
    this.elements = elements || [];
  };

  TreeNode.prototype.forEach = function(block, context) {
    for (var el = this.elements, i = 0, n = el.length; i < n; i++) {
      block.call(context, el[i], i, el);
    }
  };

  var TreeNode1 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['identifier'] = elements[0];
    this['parameters'] = elements[1];
    this['_'] = elements[3];
    this['expression'] = elements[4];
  };
  inherit(TreeNode1, TreeNode);

  var TreeNode2 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[4];
  };
  inherit(TreeNode2, TreeNode);

  var TreeNode3 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['first'] = elements[0];
    this['parameter'] = elements[0];
    this['rest'] = elements[1];
  };
  inherit(TreeNode3, TreeNode);

  var TreeNode4 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[1];
    this['parameter'] = elements[2];
  };
  inherit(TreeNode4, TreeNode);

  var TreeNode5 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['identifier'] = elements[0];
    this['default'] = elements[1];
  };
  inherit(TreeNode5, TreeNode);

  var TreeNode6 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[1];
    this['literal'] = elements[2];
  };
  inherit(TreeNode6, TreeNode);

  var TreeNode7 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['identifier'] = elements[0];
    this['_'] = elements[2];
    this['expression'] = elements[3];
  };
  inherit(TreeNode7, TreeNode);

  var TreeNode8 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['identifier'] = elements[0];
    this['_'] = elements[3];
    this['picture_component'] = elements[4];
  };
  inherit(TreeNode8, TreeNode);

  var TreeNode9 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['csg_operator'] = elements[0];
    this['picture_component'] = elements[1];
  };
  inherit(TreeNode9, TreeNode);

  var TreeNode10 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[1];
  };
  inherit(TreeNode10, TreeNode);

  var TreeNode11 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['picture_set'] = elements[0];
  };
  inherit(TreeNode11, TreeNode);

  var TreeNode12 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['identifier'] = elements[0];
    this['arguments'] = elements[1];
  };
  inherit(TreeNode12, TreeNode);

  var TreeNode13 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[6];
    this['basis'] = elements[2];
    this['num_pics'] = elements[3];
  };
  inherit(TreeNode13, TreeNode);

  var TreeNode14 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[5];
    this['num_pics'] = elements[2];
  };
  inherit(TreeNode14, TreeNode);

  var TreeNode15 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['identifier'] = elements[0];
    this['arguments'] = elements[1];
  };
  inherit(TreeNode15, TreeNode);

  var TreeNode16 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[3];
  };
  inherit(TreeNode16, TreeNode);

  var TreeNode17 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['operator'] = elements[0];
    this['arguments'] = elements[1];
  };
  inherit(TreeNode17, TreeNode);

  var TreeNode18 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['semicolon'] = elements[1];
  };
  inherit(TreeNode18, TreeNode);

  var TreeNode19 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['lhs'] = elements[0];
    this['term'] = elements[0];
    this['op'] = elements[1];
    this['operator'] = elements[1];
    this['rhs'] = elements[2];
    this['expression'] = elements[2];
  };
  inherit(TreeNode19, TreeNode);

  var TreeNode20 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[4];
    this['expression'] = elements[2];
  };
  inherit(TreeNode20, TreeNode);

  var TreeNode21 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[1];
  };
  inherit(TreeNode21, TreeNode);

  var TreeNode22 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['identifier'] = elements[0];
    this['arguments'] = elements[1];
  };
  inherit(TreeNode22, TreeNode);

  var TreeNode23 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[4];
  };
  inherit(TreeNode23, TreeNode);

  var TreeNode24 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[1];
  };
  inherit(TreeNode24, TreeNode);

  var TreeNode25 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['number'] = elements[0];
    this['_'] = elements[1];
  };
  inherit(TreeNode25, TreeNode);

  var TreeNode26 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['symbol'] = elements[1];
    this['_'] = elements[2];
  };
  inherit(TreeNode26, TreeNode);

  var TreeNode27 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['digits'] = elements[0];
    this['_'] = elements[1];
  };
  inherit(TreeNode27, TreeNode);

  var TreeNode28 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['_'] = elements[1];
  };
  inherit(TreeNode28, TreeNode);

  var TreeNode29 = function(text, offset, elements) {
    TreeNode.apply(this, arguments);
    this['whitespace'] = elements[2];
  };
  inherit(TreeNode29, TreeNode);

  var FAILURE = {};

  var Grammar = {
    _read_start: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._start = this._cache._start || {};
      var cached = this._cache._start[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var remaining0 = 1, index1 = this._offset, elements0 = [], address1 = true;
      while (address1 !== FAILURE) {
        address1 = this._read_top_level();
        if (address1 !== FAILURE) {
          elements0.push(address1);
          --remaining0;
        }
      }
      if (remaining0 <= 0) {
        address0 = new TreeNode(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      } else {
        address0 = FAILURE;
      }
      this._cache._start[index0] = [address0, this._offset];
      return address0;
    },

    _read_top_level: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._top_level = this._cache._top_level || {};
      var cached = this._cache._top_level[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset;
      address0 = this._read_function_definition();
      if (address0 === FAILURE) {
        this._offset = index1;
        address0 = this._read_variable_definition();
        if (address0 === FAILURE) {
          this._offset = index1;
          address0 = this._read_picture_definition();
          if (address0 === FAILURE) {
            this._offset = index1;
          }
        }
      }
      this._cache._top_level[index0] = [address0, this._offset];
      return address0;
    },

    _read_function_definition: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._function_definition = this._cache._function_definition || {};
      var cached = this._cache._function_definition[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(5);
      var address1 = FAILURE;
      address1 = this._read_identifier();
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read_parameters();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address3 = FAILURE;
          var chunk0 = null;
          if (this._offset < this._inputSize) {
            chunk0 = this._input.substring(this._offset, this._offset + 1);
          }
          if (chunk0 === '=') {
            address3 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
            this._offset = this._offset + 1;
          } else {
            address3 = FAILURE;
            if (this._offset > this._failure) {
              this._failure = this._offset;
              this._expected = [];
            }
            if (this._offset === this._failure) {
              this._expected.push('"="');
            }
          }
          if (address3 !== FAILURE) {
            elements0[2] = address3;
            var address4 = FAILURE;
            address4 = this._read__();
            if (address4 !== FAILURE) {
              elements0[3] = address4;
              var address5 = FAILURE;
              address5 = this._read_expression();
              if (address5 !== FAILURE) {
                elements0[4] = address5;
              } else {
                elements0 = null;
                this._offset = index1;
              }
            } else {
              elements0 = null;
              this._offset = index1;
            }
          } else {
            elements0 = null;
            this._offset = index1;
          }
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode1(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._function_definition[index0] = [address0, this._offset];
      return address0;
    },

    _read_parameters: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._parameters = this._cache._parameters || {};
      var cached = this._cache._parameters[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(5);
      var address1 = FAILURE;
      var chunk0 = null;
      if (this._offset < this._inputSize) {
        chunk0 = this._input.substring(this._offset, this._offset + 1);
      }
      if (chunk0 === '(') {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
        this._offset = this._offset + 1;
      } else {
        address1 = FAILURE;
        if (this._offset > this._failure) {
          this._failure = this._offset;
          this._expected = [];
        }
        if (this._offset === this._failure) {
          this._expected.push('"("');
        }
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read__();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address3 = FAILURE;
          var index2 = this._offset;
          var index3 = this._offset, elements1 = new Array(2);
          var address4 = FAILURE;
          address4 = this._read_parameter();
          if (address4 !== FAILURE) {
            elements1[0] = address4;
            var address5 = FAILURE;
            var remaining0 = 0, index4 = this._offset, elements2 = [], address6 = true;
            while (address6 !== FAILURE) {
              var index5 = this._offset, elements3 = new Array(3);
              var address7 = FAILURE;
              var chunk1 = null;
              if (this._offset < this._inputSize) {
                chunk1 = this._input.substring(this._offset, this._offset + 1);
              }
              if (chunk1 === ',') {
                address7 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
                this._offset = this._offset + 1;
              } else {
                address7 = FAILURE;
                if (this._offset > this._failure) {
                  this._failure = this._offset;
                  this._expected = [];
                }
                if (this._offset === this._failure) {
                  this._expected.push('","');
                }
              }
              if (address7 !== FAILURE) {
                elements3[0] = address7;
                var address8 = FAILURE;
                address8 = this._read__();
                if (address8 !== FAILURE) {
                  elements3[1] = address8;
                  var address9 = FAILURE;
                  address9 = this._read_parameter();
                  if (address9 !== FAILURE) {
                    elements3[2] = address9;
                  } else {
                    elements3 = null;
                    this._offset = index5;
                  }
                } else {
                  elements3 = null;
                  this._offset = index5;
                }
              } else {
                elements3 = null;
                this._offset = index5;
              }
              if (elements3 === null) {
                address6 = FAILURE;
              } else {
                address6 = new TreeNode4(this._input.substring(index5, this._offset), index5, elements3);
                this._offset = this._offset;
              }
              if (address6 !== FAILURE) {
                elements2.push(address6);
                --remaining0;
              }
            }
            if (remaining0 <= 0) {
              address5 = new TreeNode(this._input.substring(index4, this._offset), index4, elements2);
              this._offset = this._offset;
            } else {
              address5 = FAILURE;
            }
            if (address5 !== FAILURE) {
              elements1[1] = address5;
            } else {
              elements1 = null;
              this._offset = index3;
            }
          } else {
            elements1 = null;
            this._offset = index3;
          }
          if (elements1 === null) {
            address3 = FAILURE;
          } else {
            address3 = new TreeNode3(this._input.substring(index3, this._offset), index3, elements1);
            this._offset = this._offset;
          }
          if (address3 === FAILURE) {
            address3 = new TreeNode(this._input.substring(index2, index2), index2);
            this._offset = index2;
          }
          if (address3 !== FAILURE) {
            elements0[2] = address3;
            var address10 = FAILURE;
            var chunk2 = null;
            if (this._offset < this._inputSize) {
              chunk2 = this._input.substring(this._offset, this._offset + 1);
            }
            if (chunk2 === ')') {
              address10 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
              this._offset = this._offset + 1;
            } else {
              address10 = FAILURE;
              if (this._offset > this._failure) {
                this._failure = this._offset;
                this._expected = [];
              }
              if (this._offset === this._failure) {
                this._expected.push('")"');
              }
            }
            if (address10 !== FAILURE) {
              elements0[3] = address10;
              var address11 = FAILURE;
              address11 = this._read__();
              if (address11 !== FAILURE) {
                elements0[4] = address11;
              } else {
                elements0 = null;
                this._offset = index1;
              }
            } else {
              elements0 = null;
              this._offset = index1;
            }
          } else {
            elements0 = null;
            this._offset = index1;
          }
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = this._actions.parameters(this._input, index1, this._offset, elements0);
        this._offset = this._offset;
      }
      this._cache._parameters[index0] = [address0, this._offset];
      return address0;
    },

    _read_parameter: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._parameter = this._cache._parameter || {};
      var cached = this._cache._parameter[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      address1 = this._read_identifier();
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        var index2 = this._offset;
        var index3 = this._offset, elements1 = new Array(3);
        var address3 = FAILURE;
        var chunk0 = null;
        if (this._offset < this._inputSize) {
          chunk0 = this._input.substring(this._offset, this._offset + 1);
        }
        if (chunk0 === '=') {
          address3 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
          this._offset = this._offset + 1;
        } else {
          address3 = FAILURE;
          if (this._offset > this._failure) {
            this._failure = this._offset;
            this._expected = [];
          }
          if (this._offset === this._failure) {
            this._expected.push('"="');
          }
        }
        if (address3 !== FAILURE) {
          elements1[0] = address3;
          var address4 = FAILURE;
          address4 = this._read__();
          if (address4 !== FAILURE) {
            elements1[1] = address4;
            var address5 = FAILURE;
            address5 = this._read_literal();
            if (address5 !== FAILURE) {
              elements1[2] = address5;
            } else {
              elements1 = null;
              this._offset = index3;
            }
          } else {
            elements1 = null;
            this._offset = index3;
          }
        } else {
          elements1 = null;
          this._offset = index3;
        }
        if (elements1 === null) {
          address2 = FAILURE;
        } else {
          address2 = new TreeNode6(this._input.substring(index3, this._offset), index3, elements1);
          this._offset = this._offset;
        }
        if (address2 === FAILURE) {
          address2 = new TreeNode(this._input.substring(index2, index2), index2);
          this._offset = index2;
        }
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = this._actions.parameter(this._input, index1, this._offset, elements0);
        this._offset = this._offset;
      }
      this._cache._parameter[index0] = [address0, this._offset];
      return address0;
    },

    _read_variable_definition: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._variable_definition = this._cache._variable_definition || {};
      var cached = this._cache._variable_definition[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(4);
      var address1 = FAILURE;
      address1 = this._read_identifier();
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        var chunk0 = null;
        if (this._offset < this._inputSize) {
          chunk0 = this._input.substring(this._offset, this._offset + 1);
        }
        if (chunk0 === '=') {
          address2 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
          this._offset = this._offset + 1;
        } else {
          address2 = FAILURE;
          if (this._offset > this._failure) {
            this._failure = this._offset;
            this._expected = [];
          }
          if (this._offset === this._failure) {
            this._expected.push('"="');
          }
        }
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address3 = FAILURE;
          address3 = this._read__();
          if (address3 !== FAILURE) {
            elements0[2] = address3;
            var address4 = FAILURE;
            address4 = this._read_expression();
            if (address4 !== FAILURE) {
              elements0[3] = address4;
            } else {
              elements0 = null;
              this._offset = index1;
            }
          } else {
            elements0 = null;
            this._offset = index1;
          }
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode7(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._variable_definition[index0] = [address0, this._offset];
      return address0;
    },

    _read_picture_definition: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._picture_definition = this._cache._picture_definition || {};
      var cached = this._cache._picture_definition[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(6);
      var address1 = FAILURE;
      address1 = this._read_identifier();
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        var index2 = this._offset;
        address2 = this._read_parameters();
        if (address2 === FAILURE) {
          address2 = new TreeNode(this._input.substring(index2, index2), index2);
          this._offset = index2;
        }
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address3 = FAILURE;
          var chunk0 = null;
          if (this._offset < this._inputSize) {
            chunk0 = this._input.substring(this._offset, this._offset + 2);
          }
          if (chunk0 === '<<') {
            address3 = new TreeNode(this._input.substring(this._offset, this._offset + 2), this._offset);
            this._offset = this._offset + 2;
          } else {
            address3 = FAILURE;
            if (this._offset > this._failure) {
              this._failure = this._offset;
              this._expected = [];
            }
            if (this._offset === this._failure) {
              this._expected.push('"<<"');
            }
          }
          if (address3 !== FAILURE) {
            elements0[2] = address3;
            var address4 = FAILURE;
            address4 = this._read__();
            if (address4 !== FAILURE) {
              elements0[3] = address4;
              var address5 = FAILURE;
              address5 = this._read_picture_component();
              if (address5 !== FAILURE) {
                elements0[4] = address5;
                var address6 = FAILURE;
                var remaining0 = 0, index3 = this._offset, elements1 = [], address7 = true;
                while (address7 !== FAILURE) {
                  var index4 = this._offset, elements2 = new Array(2);
                  var address8 = FAILURE;
                  address8 = this._read_csg_operator();
                  if (address8 !== FAILURE) {
                    elements2[0] = address8;
                    var address9 = FAILURE;
                    address9 = this._read_picture_component();
                    if (address9 !== FAILURE) {
                      elements2[1] = address9;
                    } else {
                      elements2 = null;
                      this._offset = index4;
                    }
                  } else {
                    elements2 = null;
                    this._offset = index4;
                  }
                  if (elements2 === null) {
                    address7 = FAILURE;
                  } else {
                    address7 = new TreeNode9(this._input.substring(index4, this._offset), index4, elements2);
                    this._offset = this._offset;
                  }
                  if (address7 !== FAILURE) {
                    elements1.push(address7);
                    --remaining0;
                  }
                }
                if (remaining0 <= 0) {
                  address6 = new TreeNode(this._input.substring(index3, this._offset), index3, elements1);
                  this._offset = this._offset;
                } else {
                  address6 = FAILURE;
                }
                if (address6 !== FAILURE) {
                  elements0[5] = address6;
                } else {
                  elements0 = null;
                  this._offset = index1;
                }
              } else {
                elements0 = null;
                this._offset = index1;
              }
            } else {
              elements0 = null;
              this._offset = index1;
            }
          } else {
            elements0 = null;
            this._offset = index1;
          }
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode8(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._picture_definition[index0] = [address0, this._offset];
      return address0;
    },

    _read_csg_operator: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._csg_operator = this._cache._csg_operator || {};
      var cached = this._cache._csg_operator[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      var index2 = this._offset;
      var chunk0 = null;
      if (this._offset < this._inputSize) {
        chunk0 = this._input.substring(this._offset, this._offset + 2);
      }
      if (chunk0 === '++') {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset + 2), this._offset);
        this._offset = this._offset + 2;
      } else {
        address1 = FAILURE;
        if (this._offset > this._failure) {
          this._failure = this._offset;
          this._expected = [];
        }
        if (this._offset === this._failure) {
          this._expected.push('"++"');
        }
      }
      if (address1 === FAILURE) {
        this._offset = index2;
        var chunk1 = null;
        if (this._offset < this._inputSize) {
          chunk1 = this._input.substring(this._offset, this._offset + 2);
        }
        if (chunk1 === '--') {
          address1 = new TreeNode(this._input.substring(this._offset, this._offset + 2), this._offset);
          this._offset = this._offset + 2;
        } else {
          address1 = FAILURE;
          if (this._offset > this._failure) {
            this._failure = this._offset;
            this._expected = [];
          }
          if (this._offset === this._failure) {
            this._expected.push('"--"');
          }
        }
        if (address1 === FAILURE) {
          this._offset = index2;
          var chunk2 = null;
          if (this._offset < this._inputSize) {
            chunk2 = this._input.substring(this._offset, this._offset + 2);
          }
          if (chunk2 === '&&') {
            address1 = new TreeNode(this._input.substring(this._offset, this._offset + 2), this._offset);
            this._offset = this._offset + 2;
          } else {
            address1 = FAILURE;
            if (this._offset > this._failure) {
              this._failure = this._offset;
              this._expected = [];
            }
            if (this._offset === this._failure) {
              this._expected.push('"&&"');
            }
          }
          if (address1 === FAILURE) {
            this._offset = index2;
          }
        }
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read__();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode10(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._csg_operator[index0] = [address0, this._offset];
      return address0;
    },

    _read_picture_component: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._picture_component = this._cache._picture_component || {};
      var cached = this._cache._picture_component[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset;
      var index2 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      address1 = this._read_picture_set();
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        var remaining0 = 0, index3 = this._offset, elements1 = [], address3 = true;
        while (address3 !== FAILURE) {
          address3 = this._read_transform_set();
          if (address3 !== FAILURE) {
            elements1.push(address3);
            --remaining0;
          }
        }
        if (remaining0 <= 0) {
          address2 = new TreeNode(this._input.substring(index3, this._offset), index3, elements1);
          this._offset = this._offset;
        } else {
          address2 = FAILURE;
        }
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index2;
        }
      } else {
        elements0 = null;
        this._offset = index2;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode11(this._input.substring(index2, this._offset), index2, elements0);
        this._offset = this._offset;
      }
      if (address0 === FAILURE) {
        this._offset = index1;
        var index4 = this._offset, elements2 = new Array(2);
        var address4 = FAILURE;
        address4 = this._read_identifier();
        if (address4 !== FAILURE) {
          elements2[0] = address4;
          var address5 = FAILURE;
          address5 = this._read_arguments();
          if (address5 !== FAILURE) {
            elements2[1] = address5;
          } else {
            elements2 = null;
            this._offset = index4;
          }
        } else {
          elements2 = null;
          this._offset = index4;
        }
        if (elements2 === null) {
          address0 = FAILURE;
        } else {
          address0 = new TreeNode12(this._input.substring(index4, this._offset), index4, elements2);
          this._offset = this._offset;
        }
        if (address0 === FAILURE) {
          this._offset = index1;
        }
      }
      this._cache._picture_component[index0] = [address0, this._offset];
      return address0;
    },

    _read_picture_set: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._picture_set = this._cache._picture_set || {};
      var cached = this._cache._picture_set[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(7);
      var address1 = FAILURE;
      var chunk0 = null;
      if (this._offset < this._inputSize) {
        chunk0 = this._input.substring(this._offset, this._offset + 1);
      }
      if (chunk0 === '[') {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
        this._offset = this._offset + 1;
      } else {
        address1 = FAILURE;
        if (this._offset > this._failure) {
          this._failure = this._offset;
          this._expected = [];
        }
        if (this._offset === this._failure) {
          this._expected.push('"["');
        }
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read__();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address3 = FAILURE;
          address3 = this._read_basis();
          if (address3 !== FAILURE) {
            elements0[2] = address3;
            var address4 = FAILURE;
            address4 = this._read_num_pics();
            if (address4 !== FAILURE) {
              elements0[3] = address4;
              var address5 = FAILURE;
              var remaining0 = 0, index2 = this._offset, elements1 = [], address6 = true;
              while (address6 !== FAILURE) {
                address6 = this._read_transformation();
                if (address6 !== FAILURE) {
                  elements1.push(address6);
                  --remaining0;
                }
              }
              if (remaining0 <= 0) {
                address5 = new TreeNode(this._input.substring(index2, this._offset), index2, elements1);
                this._offset = this._offset;
              } else {
                address5 = FAILURE;
              }
              if (address5 !== FAILURE) {
                elements0[4] = address5;
                var address7 = FAILURE;
                var chunk1 = null;
                if (this._offset < this._inputSize) {
                  chunk1 = this._input.substring(this._offset, this._offset + 1);
                }
                if (chunk1 === ']') {
                  address7 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
                  this._offset = this._offset + 1;
                } else {
                  address7 = FAILURE;
                  if (this._offset > this._failure) {
                    this._failure = this._offset;
                    this._expected = [];
                  }
                  if (this._offset === this._failure) {
                    this._expected.push('"]"');
                  }
                }
                if (address7 !== FAILURE) {
                  elements0[5] = address7;
                  var address8 = FAILURE;
                  address8 = this._read__();
                  if (address8 !== FAILURE) {
                    elements0[6] = address8;
                  } else {
                    elements0 = null;
                    this._offset = index1;
                  }
                } else {
                  elements0 = null;
                  this._offset = index1;
                }
              } else {
                elements0 = null;
                this._offset = index1;
              }
            } else {
              elements0 = null;
              this._offset = index1;
            }
          } else {
            elements0 = null;
            this._offset = index1;
          }
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode13(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._picture_set[index0] = [address0, this._offset];
      return address0;
    },

    _read_transform_set: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._transform_set = this._cache._transform_set || {};
      var cached = this._cache._transform_set[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(6);
      var address1 = FAILURE;
      var chunk0 = null;
      if (this._offset < this._inputSize) {
        chunk0 = this._input.substring(this._offset, this._offset + 1);
      }
      if (chunk0 === '[') {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
        this._offset = this._offset + 1;
      } else {
        address1 = FAILURE;
        if (this._offset > this._failure) {
          this._failure = this._offset;
          this._expected = [];
        }
        if (this._offset === this._failure) {
          this._expected.push('"["');
        }
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read__();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address3 = FAILURE;
          address3 = this._read_num_pics();
          if (address3 !== FAILURE) {
            elements0[2] = address3;
            var address4 = FAILURE;
            var remaining0 = 0, index2 = this._offset, elements1 = [], address5 = true;
            while (address5 !== FAILURE) {
              address5 = this._read_transformation();
              if (address5 !== FAILURE) {
                elements1.push(address5);
                --remaining0;
              }
            }
            if (remaining0 <= 0) {
              address4 = new TreeNode(this._input.substring(index2, this._offset), index2, elements1);
              this._offset = this._offset;
            } else {
              address4 = FAILURE;
            }
            if (address4 !== FAILURE) {
              elements0[3] = address4;
              var address6 = FAILURE;
              var chunk1 = null;
              if (this._offset < this._inputSize) {
                chunk1 = this._input.substring(this._offset, this._offset + 1);
              }
              if (chunk1 === ']') {
                address6 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
                this._offset = this._offset + 1;
              } else {
                address6 = FAILURE;
                if (this._offset > this._failure) {
                  this._failure = this._offset;
                  this._expected = [];
                }
                if (this._offset === this._failure) {
                  this._expected.push('"]"');
                }
              }
              if (address6 !== FAILURE) {
                elements0[4] = address6;
                var address7 = FAILURE;
                address7 = this._read__();
                if (address7 !== FAILURE) {
                  elements0[5] = address7;
                } else {
                  elements0 = null;
                  this._offset = index1;
                }
              } else {
                elements0 = null;
                this._offset = index1;
              }
            } else {
              elements0 = null;
              this._offset = index1;
            }
          } else {
            elements0 = null;
            this._offset = index1;
          }
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode14(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._transform_set[index0] = [address0, this._offset];
      return address0;
    },

    _read_basis: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._basis = this._cache._basis || {};
      var cached = this._cache._basis[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      address1 = this._read_identifier();
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read_arguments();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode15(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._basis[index0] = [address0, this._offset];
      return address0;
    },

    _read_num_pics: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._num_pics = this._cache._num_pics || {};
      var cached = this._cache._num_pics[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(4);
      var address1 = FAILURE;
      var chunk0 = null;
      if (this._offset < this._inputSize) {
        chunk0 = this._input.substring(this._offset, this._offset + 1);
      }
      if (chunk0 === '{') {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
        this._offset = this._offset + 1;
      } else {
        address1 = FAILURE;
        if (this._offset > this._failure) {
          this._failure = this._offset;
          this._expected = [];
        }
        if (this._offset === this._failure) {
          this._expected.push('"{"');
        }
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        var index2 = this._offset;
        address2 = this._read_literal();
        if (address2 === FAILURE) {
          this._offset = index2;
          address2 = this._read_identifier();
          if (address2 === FAILURE) {
            this._offset = index2;
          }
        }
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address3 = FAILURE;
          var chunk1 = null;
          if (this._offset < this._inputSize) {
            chunk1 = this._input.substring(this._offset, this._offset + 1);
          }
          if (chunk1 === '}') {
            address3 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
            this._offset = this._offset + 1;
          } else {
            address3 = FAILURE;
            if (this._offset > this._failure) {
              this._failure = this._offset;
              this._expected = [];
            }
            if (this._offset === this._failure) {
              this._expected.push('"}"');
            }
          }
          if (address3 !== FAILURE) {
            elements0[2] = address3;
            var address4 = FAILURE;
            address4 = this._read__();
            if (address4 !== FAILURE) {
              elements0[3] = address4;
            } else {
              elements0 = null;
              this._offset = index1;
            }
          } else {
            elements0 = null;
            this._offset = index1;
          }
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode16(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._num_pics[index0] = [address0, this._offset];
      return address0;
    },

    _read_transformation: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._transformation = this._cache._transformation || {};
      var cached = this._cache._transformation[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      address1 = this._read_operator();
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read_arguments();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode17(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._transformation[index0] = [address0, this._offset];
      return address0;
    },

    _read_expression: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._expression = this._cache._expression || {};
      var cached = this._cache._expression[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      var index2 = this._offset;
      address1 = this._read_infix();
      if (address1 === FAILURE) {
        this._offset = index2;
        address1 = this._read_invocation();
        if (address1 === FAILURE) {
          this._offset = index2;
          address1 = this._read_literal();
          if (address1 === FAILURE) {
            this._offset = index2;
            address1 = this._read_identifier();
            if (address1 === FAILURE) {
              this._offset = index2;
            }
          }
        }
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read_semicolon();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = this._actions.expression(this._input, index1, this._offset, elements0);
        this._offset = this._offset;
      }
      this._cache._expression[index0] = [address0, this._offset];
      return address0;
    },

    _read_infix: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._infix = this._cache._infix || {};
      var cached = this._cache._infix[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(3);
      var address1 = FAILURE;
      address1 = this._read_term();
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read_operator();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address3 = FAILURE;
          address3 = this._read_expression();
          if (address3 !== FAILURE) {
            elements0[2] = address3;
          } else {
            elements0 = null;
            this._offset = index1;
          }
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = this._actions.infix(this._input, index1, this._offset, elements0);
        this._offset = this._offset;
      }
      this._cache._infix[index0] = [address0, this._offset];
      return address0;
    },

    _read_term: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._term = this._cache._term || {};
      var cached = this._cache._term[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset;
      var index2 = this._offset, elements0 = new Array(5);
      var address1 = FAILURE;
      var chunk0 = null;
      if (this._offset < this._inputSize) {
        chunk0 = this._input.substring(this._offset, this._offset + 1);
      }
      if (chunk0 === '(') {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
        this._offset = this._offset + 1;
      } else {
        address1 = FAILURE;
        if (this._offset > this._failure) {
          this._failure = this._offset;
          this._expected = [];
        }
        if (this._offset === this._failure) {
          this._expected.push('"("');
        }
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read__();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address3 = FAILURE;
          address3 = this._read_expression();
          if (address3 !== FAILURE) {
            elements0[2] = address3;
            var address4 = FAILURE;
            var chunk1 = null;
            if (this._offset < this._inputSize) {
              chunk1 = this._input.substring(this._offset, this._offset + 1);
            }
            if (chunk1 === ')') {
              address4 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
              this._offset = this._offset + 1;
            } else {
              address4 = FAILURE;
              if (this._offset > this._failure) {
                this._failure = this._offset;
                this._expected = [];
              }
              if (this._offset === this._failure) {
                this._expected.push('")"');
              }
            }
            if (address4 !== FAILURE) {
              elements0[3] = address4;
              var address5 = FAILURE;
              address5 = this._read__();
              if (address5 !== FAILURE) {
                elements0[4] = address5;
              } else {
                elements0 = null;
                this._offset = index2;
              }
            } else {
              elements0 = null;
              this._offset = index2;
            }
          } else {
            elements0 = null;
            this._offset = index2;
          }
        } else {
          elements0 = null;
          this._offset = index2;
        }
      } else {
        elements0 = null;
        this._offset = index2;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode20(this._input.substring(index2, this._offset), index2, elements0);
        this._offset = this._offset;
      }
      if (address0 === FAILURE) {
        this._offset = index1;
        address0 = this._read_invocation();
        if (address0 === FAILURE) {
          this._offset = index1;
          address0 = this._read_literal();
          if (address0 === FAILURE) {
            this._offset = index1;
            address0 = this._read_identifier();
            if (address0 === FAILURE) {
              this._offset = index1;
            }
          }
        }
      }
      this._cache._term[index0] = [address0, this._offset];
      return address0;
    },

    _read_operator: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._operator = this._cache._operator || {};
      var cached = this._cache._operator[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      var chunk0 = null;
      if (this._offset < this._inputSize) {
        chunk0 = this._input.substring(this._offset, this._offset + 1);
      }
      if (chunk0 !== null && /^[\+\*\/\-\@]/.test(chunk0)) {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
        this._offset = this._offset + 1;
      } else {
        address1 = FAILURE;
        if (this._offset > this._failure) {
          this._failure = this._offset;
          this._expected = [];
        }
        if (this._offset === this._failure) {
          this._expected.push('[\\+\\*\\/\\-\\@]');
        }
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read__();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = this._actions.operator(this._input, index1, this._offset, elements0);
        this._offset = this._offset;
      }
      this._cache._operator[index0] = [address0, this._offset];
      return address0;
    },

    _read_invocation: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._invocation = this._cache._invocation || {};
      var cached = this._cache._invocation[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      address1 = this._read_identifier();
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read_arguments();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode22(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._invocation[index0] = [address0, this._offset];
      return address0;
    },

    _read_arguments: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._arguments = this._cache._arguments || {};
      var cached = this._cache._arguments[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(5);
      var address1 = FAILURE;
      var chunk0 = null;
      if (this._offset < this._inputSize) {
        chunk0 = this._input.substring(this._offset, this._offset + 1);
      }
      if (chunk0 === '(') {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
        this._offset = this._offset + 1;
      } else {
        address1 = FAILURE;
        if (this._offset > this._failure) {
          this._failure = this._offset;
          this._expected = [];
        }
        if (this._offset === this._failure) {
          this._expected.push('"("');
        }
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read__();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address3 = FAILURE;
          var index2 = this._offset;
          var index3 = this._offset, elements1 = new Array(2);
          var address4 = FAILURE;
          var index4 = this._offset;
          address4 = this._read_expression();
          if (address4 === FAILURE) {
            address4 = new TreeNode(this._input.substring(index4, index4), index4);
            this._offset = index4;
          }
          if (address4 !== FAILURE) {
            elements1[0] = address4;
            var address5 = FAILURE;
            var remaining0 = 0, index5 = this._offset, elements2 = [], address6 = true;
            while (address6 !== FAILURE) {
              var index6 = this._offset, elements3 = new Array(3);
              var address7 = FAILURE;
              var chunk1 = null;
              if (this._offset < this._inputSize) {
                chunk1 = this._input.substring(this._offset, this._offset + 1);
              }
              if (chunk1 === ',') {
                address7 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
                this._offset = this._offset + 1;
              } else {
                address7 = FAILURE;
                if (this._offset > this._failure) {
                  this._failure = this._offset;
                  this._expected = [];
                }
                if (this._offset === this._failure) {
                  this._expected.push('","');
                }
              }
              if (address7 !== FAILURE) {
                elements3[0] = address7;
                var address8 = FAILURE;
                address8 = this._read__();
                if (address8 !== FAILURE) {
                  elements3[1] = address8;
                  var address9 = FAILURE;
                  var index7 = this._offset;
                  address9 = this._read_expression();
                  if (address9 === FAILURE) {
                    address9 = new TreeNode(this._input.substring(index7, index7), index7);
                    this._offset = index7;
                  }
                  if (address9 !== FAILURE) {
                    elements3[2] = address9;
                  } else {
                    elements3 = null;
                    this._offset = index6;
                  }
                } else {
                  elements3 = null;
                  this._offset = index6;
                }
              } else {
                elements3 = null;
                this._offset = index6;
              }
              if (elements3 === null) {
                address6 = FAILURE;
              } else {
                address6 = new TreeNode24(this._input.substring(index6, this._offset), index6, elements3);
                this._offset = this._offset;
              }
              if (address6 !== FAILURE) {
                elements2.push(address6);
                --remaining0;
              }
            }
            if (remaining0 <= 0) {
              address5 = new TreeNode(this._input.substring(index5, this._offset), index5, elements2);
              this._offset = this._offset;
            } else {
              address5 = FAILURE;
            }
            if (address5 !== FAILURE) {
              elements1[1] = address5;
            } else {
              elements1 = null;
              this._offset = index3;
            }
          } else {
            elements1 = null;
            this._offset = index3;
          }
          if (elements1 === null) {
            address3 = FAILURE;
          } else {
            address3 = new TreeNode(this._input.substring(index3, this._offset), index3, elements1);
            this._offset = this._offset;
          }
          if (address3 === FAILURE) {
            address3 = new TreeNode(this._input.substring(index2, index2), index2);
            this._offset = index2;
          }
          if (address3 !== FAILURE) {
            elements0[2] = address3;
            var address10 = FAILURE;
            var chunk2 = null;
            if (this._offset < this._inputSize) {
              chunk2 = this._input.substring(this._offset, this._offset + 1);
            }
            if (chunk2 === ')') {
              address10 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
              this._offset = this._offset + 1;
            } else {
              address10 = FAILURE;
              if (this._offset > this._failure) {
                this._failure = this._offset;
                this._expected = [];
              }
              if (this._offset === this._failure) {
                this._expected.push('")"');
              }
            }
            if (address10 !== FAILURE) {
              elements0[3] = address10;
              var address11 = FAILURE;
              address11 = this._read__();
              if (address11 !== FAILURE) {
                elements0[4] = address11;
              } else {
                elements0 = null;
                this._offset = index1;
              }
            } else {
              elements0 = null;
              this._offset = index1;
            }
          } else {
            elements0 = null;
            this._offset = index1;
          }
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode23(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._arguments[index0] = [address0, this._offset];
      return address0;
    },

    _read_literal: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._literal = this._cache._literal || {};
      var cached = this._cache._literal[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      address1 = this._read_number();
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read__();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = this._actions.literal(this._input, index1, this._offset, elements0);
        this._offset = this._offset;
      }
      this._cache._literal[index0] = [address0, this._offset];
      return address0;
    },

    _read_identifier: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._identifier = this._cache._identifier || {};
      var cached = this._cache._identifier[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(3);
      var address1 = FAILURE;
      var index2 = this._offset;
      address1 = this._read_number();
      this._offset = index2;
      if (address1 === FAILURE) {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset), this._offset);
        this._offset = this._offset;
      } else {
        address1 = FAILURE;
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read_symbol();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address3 = FAILURE;
          address3 = this._read__();
          if (address3 !== FAILURE) {
            elements0[2] = address3;
          } else {
            elements0 = null;
            this._offset = index1;
          }
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = this._actions.identifier(this._input, index1, this._offset, elements0);
        this._offset = this._offset;
      }
      this._cache._identifier[index0] = [address0, this._offset];
      return address0;
    },

    _read_number: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._number = this._cache._number || {};
      var cached = this._cache._number[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      address1 = this._read_digits();
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read__();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = this._actions.number(this._input, index1, this._offset, elements0);
        this._offset = this._offset;
      }
      this._cache._number[index0] = [address0, this._offset];
      return address0;
    },

    _read_symbol: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._symbol = this._cache._symbol || {};
      var cached = this._cache._symbol[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var remaining0 = 1, index1 = this._offset, elements0 = [], address1 = true;
      while (address1 !== FAILURE) {
        var chunk0 = null;
        if (this._offset < this._inputSize) {
          chunk0 = this._input.substring(this._offset, this._offset + 1);
        }
        if (chunk0 !== null && /^[^\s(),#=]/.test(chunk0)) {
          address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
          this._offset = this._offset + 1;
        } else {
          address1 = FAILURE;
          if (this._offset > this._failure) {
            this._failure = this._offset;
            this._expected = [];
          }
          if (this._offset === this._failure) {
            this._expected.push('[^\\s(),#=]');
          }
        }
        if (address1 !== FAILURE) {
          elements0.push(address1);
          --remaining0;
        }
      }
      if (remaining0 <= 0) {
        address0 = new TreeNode(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      } else {
        address0 = FAILURE;
      }
      this._cache._symbol[index0] = [address0, this._offset];
      return address0;
    },

    _read_digits: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._digits = this._cache._digits || {};
      var cached = this._cache._digits[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      var index2 = this._offset;
      var chunk0 = null;
      if (this._offset < this._inputSize) {
        chunk0 = this._input.substring(this._offset, this._offset + 1);
      }
      if (chunk0 === '-') {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
        this._offset = this._offset + 1;
      } else {
        address1 = FAILURE;
        if (this._offset > this._failure) {
          this._failure = this._offset;
          this._expected = [];
        }
        if (this._offset === this._failure) {
          this._expected.push('"-"');
        }
      }
      if (address1 === FAILURE) {
        address1 = new TreeNode(this._input.substring(index2, index2), index2);
        this._offset = index2;
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        var remaining0 = 1, index3 = this._offset, elements1 = [], address3 = true;
        while (address3 !== FAILURE) {
          var chunk1 = null;
          if (this._offset < this._inputSize) {
            chunk1 = this._input.substring(this._offset, this._offset + 1);
          }
          if (chunk1 !== null && /^[0-9\.]/.test(chunk1)) {
            address3 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
            this._offset = this._offset + 1;
          } else {
            address3 = FAILURE;
            if (this._offset > this._failure) {
              this._failure = this._offset;
              this._expected = [];
            }
            if (this._offset === this._failure) {
              this._expected.push('[0-9\\.]');
            }
          }
          if (address3 !== FAILURE) {
            elements1.push(address3);
            --remaining0;
          }
        }
        if (remaining0 <= 0) {
          address2 = new TreeNode(this._input.substring(index3, this._offset), index3, elements1);
          this._offset = this._offset;
        } else {
          address2 = FAILURE;
        }
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._digits[index0] = [address0, this._offset];
      return address0;
    },

    _read_semicolon: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._semicolon = this._cache._semicolon || {};
      var cached = this._cache._semicolon[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset;
      var index2 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      var chunk0 = null;
      if (this._offset < this._inputSize) {
        chunk0 = this._input.substring(this._offset, this._offset + 1);
      }
      if (chunk0 === ';') {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
        this._offset = this._offset + 1;
      } else {
        address1 = FAILURE;
        if (this._offset > this._failure) {
          this._failure = this._offset;
          this._expected = [];
        }
        if (this._offset === this._failure) {
          this._expected.push('";"');
        }
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        address2 = this._read__();
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index2;
        }
      } else {
        elements0 = null;
        this._offset = index2;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode28(this._input.substring(index2, this._offset), index2, elements0);
        this._offset = this._offset;
      }
      if (address0 === FAILURE) {
        address0 = new TreeNode(this._input.substring(index1, index1), index1);
        this._offset = index1;
      }
      this._cache._semicolon[index0] = [address0, this._offset];
      return address0;
    },

    _read__: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache.__ = this._cache.__ || {};
      var cached = this._cache.__[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(2);
      var address1 = FAILURE;
      var index2 = this._offset;
      address1 = this._read_whitespace();
      if (address1 === FAILURE) {
        address1 = new TreeNode(this._input.substring(index2, index2), index2);
        this._offset = index2;
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        var index3 = this._offset;
        address2 = this._read_comment();
        if (address2 === FAILURE) {
          address2 = new TreeNode(this._input.substring(index3, index3), index3);
          this._offset = index3;
        }
        if (address2 !== FAILURE) {
          elements0[1] = address2;
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = this._actions.ignore(this._input, index1, this._offset, elements0);
        this._offset = this._offset;
      }
      this._cache.__[index0] = [address0, this._offset];
      return address0;
    },

    _read_whitespace: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._whitespace = this._cache._whitespace || {};
      var cached = this._cache._whitespace[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var remaining0 = 0, index1 = this._offset, elements0 = [], address1 = true;
      while (address1 !== FAILURE) {
        var chunk0 = null;
        if (this._offset < this._inputSize) {
          chunk0 = this._input.substring(this._offset, this._offset + 1);
        }
        if (chunk0 !== null && /^[\n\s]/.test(chunk0)) {
          address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
          this._offset = this._offset + 1;
        } else {
          address1 = FAILURE;
          if (this._offset > this._failure) {
            this._failure = this._offset;
            this._expected = [];
          }
          if (this._offset === this._failure) {
            this._expected.push('[\\n\\s]');
          }
        }
        if (address1 !== FAILURE) {
          elements0.push(address1);
          --remaining0;
        }
      }
      if (remaining0 <= 0) {
        address0 = new TreeNode(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      } else {
        address0 = FAILURE;
      }
      this._cache._whitespace[index0] = [address0, this._offset];
      return address0;
    },

    _read_comment: function() {
      var address0 = FAILURE, index0 = this._offset;
      this._cache._comment = this._cache._comment || {};
      var cached = this._cache._comment[index0];
      if (cached) {
        this._offset = cached[1];
        return cached[0];
      }
      var index1 = this._offset, elements0 = new Array(3);
      var address1 = FAILURE;
      var chunk0 = null;
      if (this._offset < this._inputSize) {
        chunk0 = this._input.substring(this._offset, this._offset + 1);
      }
      if (chunk0 === '#') {
        address1 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
        this._offset = this._offset + 1;
      } else {
        address1 = FAILURE;
        if (this._offset > this._failure) {
          this._failure = this._offset;
          this._expected = [];
        }
        if (this._offset === this._failure) {
          this._expected.push('"#"');
        }
      }
      if (address1 !== FAILURE) {
        elements0[0] = address1;
        var address2 = FAILURE;
        var remaining0 = 0, index2 = this._offset, elements1 = [], address3 = true;
        while (address3 !== FAILURE) {
          var chunk1 = null;
          if (this._offset < this._inputSize) {
            chunk1 = this._input.substring(this._offset, this._offset + 1);
          }
          if (chunk1 !== null && /^[^\n]/.test(chunk1)) {
            address3 = new TreeNode(this._input.substring(this._offset, this._offset + 1), this._offset);
            this._offset = this._offset + 1;
          } else {
            address3 = FAILURE;
            if (this._offset > this._failure) {
              this._failure = this._offset;
              this._expected = [];
            }
            if (this._offset === this._failure) {
              this._expected.push('[^\\n]');
            }
          }
          if (address3 !== FAILURE) {
            elements1.push(address3);
            --remaining0;
          }
        }
        if (remaining0 <= 0) {
          address2 = new TreeNode(this._input.substring(index2, this._offset), index2, elements1);
          this._offset = this._offset;
        } else {
          address2 = FAILURE;
        }
        if (address2 !== FAILURE) {
          elements0[1] = address2;
          var address4 = FAILURE;
          address4 = this._read_whitespace();
          if (address4 !== FAILURE) {
            elements0[2] = address4;
          } else {
            elements0 = null;
            this._offset = index1;
          }
        } else {
          elements0 = null;
          this._offset = index1;
        }
      } else {
        elements0 = null;
        this._offset = index1;
      }
      if (elements0 === null) {
        address0 = FAILURE;
      } else {
        address0 = new TreeNode29(this._input.substring(index1, this._offset), index1, elements0);
        this._offset = this._offset;
      }
      this._cache._comment[index0] = [address0, this._offset];
      return address0;
    }
  };

  var Parser = function(input, actions, types) {
    this._input = input;
    this._inputSize = input.length;
    this._actions = actions;
    this._types = types;
    this._offset = 0;
    this._cache = {};
    this._failure = 0;
    this._expected = [];
  };

  Parser.prototype.parse = function() {
    var tree = this._read_start();
    if (tree !== FAILURE && this._offset === this._inputSize) {
      return tree;
    }
    if (this._expected.length === 0) {
      this._failure = this._offset;
      this._expected.push('<EOF>');
    }
    this.constructor.lastError = {offset: this._offset, expected: this._expected};
    throw new SyntaxError(formatError(this._input, this._failure, this._expected));
  };

  var parse = function(input, options) {
    options = options || {};
    var parser = new Parser(input, options.actions, options.types);
    return parser.parse();
  };
  extend(Parser.prototype, Grammar);

  var exported = {Grammar: Grammar, Parser: Parser, parse: parse};

  if (typeof require === 'function' && typeof exports === 'object') {
    extend(exports, exported);
  } else {
    var namespace = typeof this !== 'undefined' ? this : window;
    namespace.oskar = exported;
  }
})();
