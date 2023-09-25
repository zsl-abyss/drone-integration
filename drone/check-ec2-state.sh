#! /usr/bin/env bash

default_poll_attempts=50

function usage()
{
    cat << EOF
Usage:

$( basename "$0" ) instance-name [state] [poll-freq] [poll-attempts]

A simple script to check and/or optionally wait for an AWS EC2 instance state
to change to a predefined value.

    options:

        instance-name:  The AWS EC2 instance-name to check.

        state:          The state to check for.

        poll-freq:      The frequency to re-poll in seconds.

        poll-attempts:  The amount of attempts to make before exiting.
                        Specify a non-positive integer to infinately poll. By
                        default $default_poll_attempts attempts will be made
                        before exiting.

    examples:

        $( basename "$0" ) i-0000000000

            Will output the current state of an instance.

        $( basename "$0" ) i-0000000000 running

            Will output the current state of an instance and exit with a non-
            zero status code if the instance isn't in the given state.

        $( basename "$0" ) i-0000000000 running 1

            Will check the current state of the instance and re-poll every 1
            second until the desired state is reached, then exit. By
            default $default_poll_attempts attempts will be made before exiting.

        $( basename "$0" ) i-0000000000 running 1 100

            Will check the current state of the instance 100 times and re-poll
            every 1 second until the instance is running or 100 attempts have
            been made, then exit.

EOF
    exit 1
}

function get_state()
{
    check_cmd=$(aws ec2 describe-instances \
        --query "Reservations[*].Instances[*].{Status:State.Name}" \
        --filters "Name=tag:Name,Values=$instance_name" \
        --region ap-southeast-2)
    state=$(jq .[0][0].Status <(echo ${check_cmd}))
    echo $(sed 's/"//g' <(echo $state))
}

function check_state()
{
    current_state=$(get_state)
    echo $current_state
    if [[ $requested_state == $current_state ]]; then
        return 0
    else
        return 1
    fi
}

function poll_state()
{
    counter=1
    until check_state || [[ $counter == $poll_attempts ]]
    do
        sleep $poll_freq
        [[ $poll_attempts > 0 ]] && ((counter++))
    done
    state_match=check_state
    [[ $counter == $poll_attempts ]] && return 2
    return $((state_match))
}

instance_name=$1

[[ $1 == "-h" ||  $1 == "--help" ]] && usage


case $# in

    0)
        usage
        ;;

    1)
        echo $(get_state)
        ;;

    2)
        requested_state=$2
        check_states
        exit $?
        ;;

    3)
        requested_state=$2
        poll_freq=$3
        poll_attempts=$default_poll_attempts
        poll_state
        exit $?
        ;;

    4)
        requested_state=$2
        poll_freq=$3
        poll_attempts=$4
        poll_state
        exit $?
        ;;

    *)
        usage;
        ;;
esac
exit 0
