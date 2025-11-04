package org.javaboy.vhr.model;

public class MailConstants {
    public static final Integer DELIVERING = 0;
    public static final Integer SUCCESS = 1;
    public static final Integer FAILURE = 2;
    public static final Integer MAX_TRY_COUNT = 3;
    public static final Integer MSG_TIMEOUT = 1;
    public static final String MAIL_QUEUE_NAME = "javaboy.mail.queue";
    public static final String MAIL_EXCHANGE_NAME = "javaboy.mail.exchange";
    public static final String MAIL_ROUTING_KEY_NAME = "javaboy.mail.routing.key";
}
