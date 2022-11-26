type=''
name=''

while test $# -gt 0
do
    case "$1" in
        -t|--type)  type="$2"
            shift ;;
        *) name="$1" ;;
    esac
    shift
done

createProjectC() {
    echo "making c project"
}

createProject() {
    echo "creating a $type project called $name"

    if [ $type == 'c' ]
    then
        createProjectC
    else
        echo "Unknown project type"
    fi
}


createProject $*
