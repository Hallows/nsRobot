/*
 Navicat Premium Data Transfer

 Source Server         : jx3bot
 Source Server Type    : MySQL
 Source Server Version : 50733
 Source Host           : 139.198.178.48:3306
 Source Schema         : ns_db

 Target Server Type    : MySQL
 Target Server Version : 50733
 File Encoding         : 65001

 Date: 26/02/2021 00:26:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ns_leader
-- ----------------------------
DROP TABLE IF EXISTS `ns_leader`;
CREATE TABLE `ns_leader`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `QQNumber` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `nickName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `activeTime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `effective` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ns_member
-- ----------------------------
DROP TABLE IF EXISTS `ns_member`;
CREATE TABLE `ns_member`  (
  `teamID` int(11) NOT NULL,
  `memberQQ` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `memberNickname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `mentalID` int(11) NULL DEFAULT NULL,
  `syana` int(11) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ns_mental
-- ----------------------------
DROP TABLE IF EXISTS `ns_mental`;
CREATE TABLE `ns_mental`  (
  `mentalID` int(50) NOT NULL,
  `mentalName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `mentalIcon` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `acceptName` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `mentalColor` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `works` int(255) NULL DEFAULT NULL,
  `relation

Mental` int(255) NULL DEFAULT NULL,
  PRIMARY KEY (`mentalID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ns_team
-- ----------------------------
DROP TABLE IF EXISTS `ns_team`;
CREATE TABLE `ns_team`  (
  `teamID` int(11) NOT NULL AUTO_INCREMENT,
  `leaderID` int(11) NULL DEFAULT NULL,
  `dungeon` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `startDate` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `startTime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `effective` smallint(6) NULL DEFAULT NULL,
  `allowBlackList` smallint(6) NULL DEFAULT NULL,
  `remark` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`teamID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1002 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
