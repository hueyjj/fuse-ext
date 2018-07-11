ifndef $(GOPATH)
    GOPATH=$(shell go env GOPATH)
    export GOPATH
endif

all: youtube-grpc

phoney:
	echo "nothing"
	echo $(GOPATH)

youtube-grpc:
	python -m grpc_tools.protoc -I. -I$(GOPATH)/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis --python_out=. --grpc_python_out=. proto/youtube.proto

clean:
	# TODO
