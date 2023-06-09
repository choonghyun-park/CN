"""
Sender

1. When send data packet                                                : Send DATA
2. When found packet corruption                                         : DATA Corrupted
3. When sequence number is different                                    : Wrong Sequence Number
4. When retransmit data packet                                          : Send DATA Again
5. When success to receive ack packet                                   : Sent Successfully
6. When success to receive ack packet, but out of order                 : Sent Successfully: Mark
7. Timeout                                                              : (Use writeTimeout function)

Receiver

1. When found packet corruption                                         : DATA Corrupted
2. When sequence number is different                                    : Wrong Sequence Number
3. When sequence number is different, thus needs to be buffered (SR)    : Wrong Sequence Number: Buffer
4. When retransmit ACK packet                                           : Send ACK Again
5. When success to receive data packet                                  : Sent ACK
"""

SEND_DATA = "Send DATA"
CORRUPTED = "DATA Corrupted"
SEND_DATA_AGAIN = "Send DATA Again"
WRONG_SEQ_NUM = "Wrong Sequence Number"
WRONG_SEQ_NUM_BUFFER = "Wrong Sequence Number: Buffer"
SUCCESS_ACK = "Sent Successfully"
SUCCESS_ACK_MARK = "Sent Successfully: Mark"
SEND_ACK_AGAIN = "Send ACK Again"
SEND_ACK = "Send ACK"


"Use this method to write Packet log"


def writePkt(logFile, procTime, pktNum, event):
    logFile.write("{:1.3f} pkt: {} | {}\n".format(procTime, pktNum, event))
    logFile.flush()


"Use this method to write ACK log"


def writeAck(logFile, procTime, ackNum, event):
    logFile.write("{:1.3f} ACK: {} | {}\n".format(procTime, ackNum, event))
    logFile.flush()


"Use this method to write Timeout"


def writeTimeout(logFile, procTime, ackNum):
    logFile.write("{:1.3f} pkt: {} | {}\n".format(procTime, ackNum, "TIMEOUT"))
    logFile.flush()


"Use this method to write final throughput log"


def writeEnd(logFile):
    logFile.write("File transfer is finished.\n")
